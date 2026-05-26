"""
语音情绪识别系统 v2.0 - Web 版
浏览器打开 http://localhost:5000 即可使用
"""
import os
import sys
import threading
import json
import uuid
import webbrowser
from pathlib import Path

import flask
from flask import Flask, request, jsonify, render_template_string

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>语音情绪识别系统</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f0f2f5;color:#333;display:flex;flex-direction:column;align-items:center}
.container{max-width:800px;width:100%;padding:24px 16px}
.header{text-align:center;margin-bottom:20px}
.header h1{font-size:26px;font-weight:700;color:#1a1a2e}
.header p{color:#666;font-size:14px;margin-top:4px}
.card{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
.card-title{font-size:15px;font-weight:600;margin-bottom:12px;color:#1a1a2e}
.upload-zone{border:2px dashed #d0d5dd;border-radius:10px;padding:28px 16px;text-align:center;cursor:pointer;transition:all .2s;background:#fafafa}
.upload-zone:hover,.upload-zone.dragover{border-color:#6366f1;background:#f5f3ff}
.upload-zone input{display:none}
.upload-zone .icon{font-size:32px;margin-bottom:6px}
.upload-zone .text{color:#666;font-size:14px}
.upload-zone .sub{color:#999;font-size:12px;margin-top:4px}
.status-bar{display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:8px;font-size:13px;margin:0 0 12px 0;background:#f8f9ff;color:#555}
.status-bar .dot{width:8px;height:8px;border-radius:50%;background:#ccc;flex-shrink:0}
.status-bar .dot.green{background:#22c55e}
.status-bar .dot.blue{background:#6366f1;animation:pulse 1s infinite}
.status-bar .dot.red{background:#ef4444}
@keyframes pulse{50%{opacity:.4}}
.progress-wrap{width:100%;height:6px;background:#e5e7eb;border-radius:3px;margin:0 0 16px 0;overflow:hidden}
.progress-bar{height:100%;background:linear-gradient(90deg,#6366f1,#8b5cf6);border-radius:3px;transition:width .3s;width:0%}
.progress-bar.indeterminate{width:30%;animation:slide 1.5s ease-in-out infinite}
@keyframes slide{50%{width:70%;margin-left:30%}}
.tabs{display:flex;gap:8px;margin-bottom:16px}
.tab{flex:1;padding:10px;text-align:center;border-radius:8px;cursor:pointer;font-size:14px;font-weight:500;background:#e5e7eb;color:#666;transition:all .2s;border:none}
.tab.active{background:#6366f1;color:#fff}
.tab-content{display:none}
.tab-content.active{display:block}
.file-list{margin-top:10px}
.file-item{display:flex;align-items:center;gap:8px;padding:6px 10px;background:#f9fafb;border-radius:6px;font-size:13px;margin-bottom:4px}
.file-item .name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.file-item .rm{color:#999;cursor:pointer;font-size:14px}
.file-item .rm:hover{color:#ef4444}
.result-table{width:100%;border-collapse:collapse;font-size:13px;margin-top:12px}
.result-table th{background:#f8f9ff;padding:8px 10px;text-align:left;font-weight:600;border-bottom:2px solid #e5e7eb}
.result-table td{padding:8px 10px;border-bottom:1px solid #f0f0f0}
.result-table tr:hover td{background:#fafaff}
.result-table .emo{font-weight:600}
.result-table .bar-bg{display:inline-block;width:60px;height:8px;background:#e5e7eb;border-radius:4px;overflow:hidden;vertical-align:middle}
.result-table .bar-fill{height:100%;border-radius:4px}
.result-table .pct{font-size:12px;color:#888;margin-left:4px}
.batch-progress{display:none;margin:12px 0}
.batch-progress.show{display:block}
.btn{width:100%;padding:12px;border:none;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer;transition:opacity .2s;margin-bottom:12px}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-primary{background:#6366f1;color:#fff}
.btn-outline{background:transparent;border:1px solid #d0d5dd;color:#555;padding:8px 16px;font-size:13px;width:auto;border-radius:6px;cursor:pointer}
.btn-row{display:flex;gap:8px;margin-top:12px}
.footer{text-align:center;font-size:12px;color:#999;padding:16px 0}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>&#x1F3A4; 语音情绪识别</h1>
<p>基于深度学习的多语种语音情绪识别</p>
</div>

<div class="status-bar" id="statusBar">
<span class="dot blue" id="statusDot"></span>
<span id="statusText">正在加载模型...</span>
</div>
<div class="progress-wrap" id="progressWrap">
<div class="progress-bar indeterminate" id="progressBar"></div>
</div>

<div class="tabs">
<button class="tab active" onclick="switchTab('single')">单个识别</button>
<button class="tab" onclick="switchTab('batch')">批量处理</button>
</div>

<!-- 单个识别 -->
<div class="tab-content active" id="tabSingle">
<div class="card">
<div class="upload-zone" id="dropZone">
<div class="icon">&#x1F4C1;</div>
<div class="text">点击选择 或 拖放音频文件</div>
<div class="sub">WAV / MP3 / FLAC / M4A / AAC</div>
<input type="file" id="fileInput" accept=".wav,.mp3,.flac,.m4a,.aac,audio/*">
</div>
</div>
<button class="btn btn-primary" id="predictBtn" disabled onclick="predict()">等待模型加载...</button>
<div class="card" id="singleResult" style="display:none">
<div class="card-title">识别结果</div>
<div style="font-size:32px;font-weight:700;text-align:center;padding:8px 0" id="resultEmotion">--</div>
<div id="topkContainer"></div>
</div>
</div>

<!-- 批量处理 -->
<div class="tab-content" id="tabBatch">
<div class="card">
<div class="upload-zone" id="batchDropZone">
<div class="icon">&#x1F4C2;</div>
<div class="text">点击选择多个文件，或拖放</div>
<div class="sub">支持同时选择多个音频文件</div>
<input type="file" id="batchFileInput" multiple accept=".wav,.mp3,.flac,.m4a,.aac,audio/*">
</div>
<div class="file-list" id="batchFileList"></div>
</div>
<button class="btn btn-primary" id="batchBtn" disabled onclick="batchPredict()">等待模型加载...</button>
<div class="batch-progress" id="batchProgress">
<div class="status-bar" style="margin:0"><span class="dot blue"></span><span id="batchProgressText">准备中...</span></div>
<div class="progress-wrap" style="margin:8px 0 0 0"><div class="progress-bar" id="batchProgressBar" style="width:0%"></div></div>
</div>
<div class="card" id="batchResult" style="display:none">
<div class="card-title">批量结果</div>
<div id="batchStats" style="font-size:14px;color:#666;margin-bottom:8px"></div>
<div style="overflow-x:auto">
<table class="result-table"><thead><tr><th>#</th><th>文件名</th><th>情绪</th><th>置信度</th><th>Top-3</th></tr></thead><tbody id="batchTbody"></tbody></table>
</div>
<div class="btn-row">
<button class="btn-outline" onclick="downloadCSV()">&#x1F4E5; 下载 CSV</button>
</div>
</div>
</div>

<div class="footer">语音情绪识别系统 v2.0</div>
</div>

<script>
const ACCEPT=[".wav",".mp3",".flac",".m4a",".aac"];
let modelReady=false,batchFiles=[],batchResults=[];

async function pollStatus(){
try{
const r=await fetch("/api/status");const d=await r.json();
const dot=document.getElementById("statusDot"),txt=document.getElementById("statusText"),pb=document.getElementById("progressBar"),pw=document.getElementById("progressWrap");
if(d.status==="ready"){
modelReady=true;dot.className="dot green";txt.textContent="就绪 · "+(d.model||"");pb.className="progress-bar";pb.style.width="100%";
setTimeout(()=>pw.style.display="none",500);updateButtons();
}else if(d.status==="loading"){
dot.className="dot blue";txt.textContent=d.message||"加载中...";
pb.className=d.progress>0?"progress-bar":"progress-bar indeterminate";
if(d.progress>0)pb.style.width=d.progress+"%";
setTimeout(pollStatus,500);
}else if(d.status==="error"){
dot.className="dot red";txt.textContent="失败: "+(d.message||"");setTimeout(pollStatus,3000);
}else{setTimeout(pollStatus,500);}
}catch(e){setTimeout(pollStatus,1000);}
}
pollStatus();

function updateButtons(){
const pr=document.getElementById("predictBtn"),bt=document.getElementById("batchBtn");
if(!modelReady){pr.textContent="模型加载中...";pr.disabled=true;bt.textContent="模型加载中...";bt.disabled=true;return;}
pr.textContent="&#x1F3A4; 识别情绪";pr.disabled=!document.getElementById("fileInput").files.length;
bt.textContent="&#x1F4C2; 批量识别";bt.disabled=batchFiles.length===0;
}

function switchTab(name){
document.querySelectorAll(".tab").forEach(t=>t.classList.remove("active"));
document.querySelectorAll(".tab-content").forEach(t=>t.classList.remove("active"));
if(name==="single"){document.querySelectorAll(".tab")[0].classList.add("active");document.getElementById("tabSingle").classList.add("active");}
else{document.querySelectorAll(".tab")[1].classList.add("active");document.getElementById("tabBatch").classList.add("active");}
}

// 单文件
const dz=document.getElementById("dropZone"),fi=document.getElementById("fileInput");
dz.onclick=()=>fi.click();
dz.ondragover=e=>{e.preventDefault();dz.classList.add("dragover");};
dz.ondragleave=()=>dz.classList.remove("dragover");
dz.ondrop=e=>{e.preventDefault();dz.classList.remove("dragover");if(e.dataTransfer.files[0])handleSingleFile(e.dataTransfer.files[0]);};
fi.onchange=()=>{if(fi.files[0])handleSingleFile(fi.files[0]);};

function handleSingleFile(f){
const ext="."+f.name.split(".").pop().toLowerCase();
if(!ACCEPT.includes(ext)){alert("不支持: "+ext);return;}
document.getElementById("singleResult").style.display="none";
updateButtons();
}

async function predict(){
if(!modelReady||!fi.files.length)return;
const btn=document.getElementById("predictBtn");btn.textContent="&#x23F3; 识别中...";btn.disabled=true;
const fd=new FormData();fd.append("audio",fi.files[0]);
try{
const r=await fetch("/api/predict",{method:"POST",body:fd});const d=await r.json();
if(d.error){alert("出错: "+d.error);return;}
showResult(d);
}catch(e){alert("请求失败: "+e.message);}
finally{updateButtons();}
}

function showResult(d){
document.getElementById("singleResult").style.display="block";
document.getElementById("resultEmotion").textContent=d.emotion+"  ("+(d.confidence*100).toFixed(1)+"%)";
const colors=["#6366f1","#8b5cf6","#a855f7","#d946ef","#ec4899","#f43f5e","#ef4444","#f97316"];
let html="";
d.top_k.forEach((item,i)=>{
const pct=(item.score*100).toFixed(1);
html+='<div style="display:flex;align-items:center;gap:12px;margin:6px 0">';
html+='<div style="width:70px;font-size:14px;text-align:right">'+item.label+'</div>';
html+='<div style="flex:1;height:22px;background:#e5e7eb;border-radius:6px;overflow:hidden">';
html+='<div style="height:100%;border-radius:6px;width:'+pct+'%;background:'+colors[i%colors.length]+';display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-size:11px;color:#fff;font-weight:600">'+pct+'%</div></div>';
html+='<div style="width:50px;font-size:12px;color:#888">'+item.score.toFixed(4)+'</div></div>';
});
document.getElementById("topkContainer").innerHTML=html;
}

// 批量
const bdz=document.getElementById("batchDropZone"),bfi=document.getElementById("batchFileInput");
bdz.onclick=()=>bfi.click();
bdz.ondragover=e=>{e.preventDefault();bdz.classList.add("dragover");};
bdz.ondragleave=()=>bdz.classList.remove("dragover");
bdz.ondrop=e=>{e.preventDefault();bdz.classList.remove("dragover");addBatchFiles(e.dataTransfer.files);};
bfi.onchange=()=>{addBatchFiles(bfi.files);bfi.value="";};

function addBatchFiles(files){
for(const f of files){
const ext="."+f.name.split(".").pop().toLowerCase();
if(ACCEPT.includes(ext))batchFiles.push(f);
}
renderBatchFiles();updateButtons();
}

function removeBatchFile(idx){batchFiles.splice(idx,1);renderBatchFiles();updateButtons();}

function renderBatchFiles(){
const el=document.getElementById("batchFileList");
if(batchFiles.length===0){el.innerHTML="";return;}
let h='<div style="font-size:13px;color:#888;margin-bottom:6px">共 '+batchFiles.length+' 个文件</div>';
batchFiles.forEach((f,i)=>{
h+='<div class="file-item"><span class="name">'+f.name+' ('+(f.size/1024/1024).toFixed(1)+' MB)</span><span class="rm" onclick="removeBatchFile('+i+')">&#x2715;</span></div>';
});
el.innerHTML=h;
}

async function batchPredict(){
if(!modelReady||batchFiles.length===0)return;
batchResults=[];document.getElementById("batchResult").style.display="none";
document.getElementById("batchProgress").classList.add("show");
const bar=document.getElementById("batchProgressBar"),txt=document.getElementById("batchProgressText");
const btn=document.getElementById("batchBtn");btn.disabled=true;
for(let i=0;i<batchFiles.length;i++){
const pct=((i)/batchFiles.length*100).toFixed(0);
bar.style.width=pct+"%";
txt.textContent="["+(i+1)+"/"+batchFiles.length+"] "+batchFiles[i].name;
const fd=new FormData();fd.append("audio",batchFiles[i]);
try{
const r=await fetch("/api/predict",{method:"POST",body:fd});const d=await r.json();
batchResults.push({file:batchFiles[i].name,result:d.error?{error:d.error}:d});
}catch(e){batchResults.push({file:batchFiles[i].name,result:{error:e.message}});
}}
bar.style.width="100%";txt.textContent="处理完成! 共 "+batchFiles.length+" 个文件";
document.getElementById("batchProgress").classList.remove("show");
document.getElementById("batchResult").style.display="block";
renderBatchResults();btn.disabled=false;updateButtons();
}

function renderBatchResults(){
const ok=batchResults.filter(r=>!r.result.error);
const err=batchResults.filter(r=>r.result.error);
document.getElementById("batchStats").textContent="成功 "+ok.length+" / 失败 "+err.length+" / 总计 "+batchResults.length;
const colors=["#6366f1","#8b5cf6","#a855f7","#d946ef","#ec4899","#f43f5e","#ef4444","#f97316"];
let h="";
batchResults.forEach((r,i)=>{
h+="<tr><td>"+(i+1)+"</td><td>"+r.file+"</td>";
if(r.result.error){
h+='<td style="color:#ef4444">失败</td><td>-</td><td style="font-size:12px;color:#999">'+r.result.error+"</td>";
}else{
const conf=(r.result.confidence*100).toFixed(1);
const top=r.result.top_k||[];
const detail=top.slice(0,3).map(t=>t.label+" "+(t.score*100).toFixed(0)+"%").join(" | ");
h+='<td class="emo">'+r.result.emotion+"</td>";
h+='<td><span class="bar-bg"><span class="bar-fill" style="width:'+conf+'%;background:'+colors[0]+'"></span></span><span class="pct">'+conf+"%</span></td>";
h+='<td style="font-size:12px;color:#888">'+detail+"</td>";
}
h+="</tr>";
});
document.getElementById("batchTbody").innerHTML=h;
}

function downloadCSV(){
let csv="\\uFEFF文件名,情绪,置信度,Top-3\\n";
batchResults.forEach(r=>{
if(r.result.error){csv+=r.file+",失败,0,"+r.result.error+"\\n";}
else{
const detail=(r.result.top_k||[]).map(t=>t.label+":"+(t.score*100).toFixed(1)+"%").join("; ");
csv+=r.file+","+r.result.emotion+","+(r.result.confidence*100).toFixed(1)+"%,"+detail+"\\n";
}
});
const blob=new Blob([csv],{type:"text/csv;charset=utf-8"});
const url=URL.createObjectURL(blob);
const a=document.createElement("a");a.href=url;a.download="emotion_results.csv";a.click();URL.revokeObjectURL(url);
}
</script>
</body>
</html>"""

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024

recognizer = None
model_status = {"status": "init", "message": "正在初始化...", "progress": 0, "model": ""}
UPLOAD_DIR = Path(__file__).parent / ".uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def load_model_thread():
    global recognizer, model_status
    try:
        model_status = {"status": "loading", "message": "正在连接...", "progress": 0, "model": ""}
        def on_progress(fn, cur, total):
            if total > 0:
                pct = min(cur / total * 100, 99.9)
                model_status["progress"] = int(pct)
                model_status["message"] = f"下载: {fn} ({pct:.0f}%)"
        from emotion_recognizer import EmotionRecognizer
        recognizer = EmotionRecognizer(progress_callback=on_progress)
        model_status = {"status": "ready", "message": "就绪", "progress": 100, "model": recognizer.model_name.split("/")[-1]}
    except Exception as e:
        model_status = {"status": "error", "message": str(e), "progress": 0, "model": ""}


@app.route("/")
def index():
    return render_template_string(PAGE_HTML)


@app.route("/api/status")
def api_status():
    return jsonify(model_status)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    global recognizer
    if not recognizer:
        return jsonify({"error": "模型未加载完成"}), 503
    if "audio" not in request.files:
        return jsonify({"error": "请上传音频"}), 400

    f = request.files["audio"]
    ext = os.path.splitext(f.filename or "audio.wav")[1] or ".wav"
    tmp = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
    f.save(tmp)
    try:
        emotion, confidence = recognizer.predict_emotion(str(tmp))
        top_k = recognizer.predict_emotions(str(tmp), top_k=5)
        return jsonify({
            "emotion": emotion,
            "confidence": round(confidence, 4),
            "top_k": [{"label": e, "score": round(s, 4)} for e, s in top_k],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(tmp)


if __name__ == "__main__":
    print("=" * 50)
    print("  语音情绪识别系统 v2.0 - Web 版")
    print(f"  浏览器打开: http://localhost:5000")
    print("  Ctrl+C 退出")
    print("=" * 50)
    threading.Thread(target=load_model_thread, daemon=True).start()
    threading.Timer(1.5, lambda: webbrowser.open("http://localhost:5000")).start()
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
