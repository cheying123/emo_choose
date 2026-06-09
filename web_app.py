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

# ===== HTML 页面 =====
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
.status-bar .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
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
.result-table .tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
.batch-progress{display:none;margin:12px 0}
.batch-progress.show{display:block}
.btn{width:100%;padding:12px;border:none;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer;transition:opacity .2s;margin-bottom:12px}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-primary{background:#6366f1;color:#fff}
.btn-success{background:#22c55e;color:#fff}
.btn-warning{background:#f59e0b;color:#fff}
.btn-outline{background:transparent;border:1px solid #d0d5dd;color:#555;padding:8px 16px;font-size:13px;width:auto;border-radius:6px;cursor:pointer}
.btn-row{display:flex;gap:8px;margin-top:12px}
.footer{text-align:center;font-size:12px;color:#999;padding:16px 0}
.rank-card{border:1px solid #e5e7eb;border-radius:10px;padding:16px;margin-bottom:12px}
.rank-card.top1{border-color:#f59e0b;background:#fffbeb}
.rank-card.top2{border-color:#d0d5dd;background:#f9fafb}
.rank-badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:700}
.rank-badge.gold{background:#f59e0b;color:#fff}
.rank-badge.silver{background:#9ca3af;color:#fff}
.ai-score{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.ai-score-item{text-align:center;min-width:70px}
.ai-score-val{font-size:22px;font-weight:700;color:#6366f1}
.ai-score-label{font-size:11px;color:#888;margin-top:2px}
.ai-reason{font-size:13px;color:#555;margin-top:8px;padding:8px 12px;background:#fff;border-radius:6px;border:1px solid #e5e7eb}
.tag-neutral{background:#e0e7ff;color:#4338ca}
.tag-good{background:#d1fae5;color:#065f46}
.tag-best{background:#fef3c7;color:#92400e}</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>&#x1F3A4; 语音情绪识别系统</h1>
<p>多语种语音情绪分析 · AI 参考音频推荐</p>
</div>

<div class="status-bar" id="statusBar">
<span class="dot blue" id="statusDot"></span>
<span id="statusText">正在加载模型...</span>
</div>
<div class="progress-wrap" id="progressWrap">
<div class="progress-bar indeterminate" id="progressBar"></div>
</div>

<div class="tabs">
<button class="tab active" onclick="switchTab('single')">&#x1F3A4; 单文件</button>
<button class="tab" onclick="switchTab('batch')">&#x1F4CB; 批量</button>
<button class="tab" onclick="switchTab('analyze')">&#x1F9E0; AI 分析</button>
</div>

<!-- 单文件 -->
<div class="tab-content active" id="tabSingle">
<div class="card">
<div class="upload-zone" id="dropZone">
<div class="icon">&#x1F4C1;</div><div class="text">点击或拖放音频文件</div>
<div class="sub">WAV / MP3 / FLAC / M4A / AAC</div>
<input type="file" id="fileInput" accept=".wav,.mp3,.flac,.m4a,.aac,audio/*">
</div></div>
<button class="btn btn-primary" id="predictBtn" disabled onclick="predict()">等待模型加载...</button>
<div class="card" id="singleResult" style="display:none">
<div class="card-title">识别结果</div>
<div style="font-size:32px;font-weight:700;text-align:center;padding:8px 0" id="resultEmotion">--</div>
<div id="topkContainer"></div>
</div></div>

<!-- 批量 -->
<div class="tab-content" id="tabBatch">
<div class="card">
<div class="upload-zone" id="batchDropZone">
<div class="icon">&#x1F4C2;</div><div class="text">点击选择多个文件或拖放</div>
<div class="sub">支持同时选择多个</div>
<input type="file" id="batchFileInput" multiple accept=".wav,.mp3,.flac,.m4a,.aac,audio/*">
</div>
<button class="btn btn-primary" id="batchBtn" disabled onclick="batchPredict()">等待模型加载...</button>
<div class="file-list" id="batchFileList"></div></div>
<div class="batch-progress" id="batchProgress">
<div class="status-bar" style="margin:0"><span class="dot blue"></span><span id="batchProgressText">准备中...</span></div>
<div class="progress-wrap" style="margin:8px 0 0 0"><div class="progress-bar" id="batchProgressBar" style="width:0%"></div></div></div>
<div class="card" id="batchResult" style="display:none">
<div class="card-title">批量结果</div>
<div id="batchStats" style="font-size:14px;color:#666;margin-bottom:8px"></div>
<div style="overflow-x:auto"><table class="result-table"><thead><tr><th>#</th><th>文件名</th><th>情绪</th><th>置信度</th><th>Top-3</th></tr></thead><tbody id="batchTbody"></tbody></table></div>
<div class="btn-row"><button class="btn-outline" onclick="downloadCSV()">&#x1F4E5; 下载 CSV</button></div>
</div></div>

<!-- AI 分析 -->
<div class="tab-content" id="tabAnalyze">
<div class="card">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
<div style="font-size:28px">&#x1F916;</div>
<div><div style="font-weight:600;font-size:15px">AI 参考音频分析</div>
<div style="font-size:12px;color:#888">输入台词 + 上传多条音频，AI 分析哪个版本情绪表达最到位</div></div></div>

<div style="margin-bottom:8px"><strong style="font-size:14px">&#x1F4DD; 1. 输入台词文本</strong>
<div style="font-size:12px;color:#888;margin-bottom:4px">每行一段话，用于分析文本预期情绪</div></div>
<textarea id="scriptInput" placeholder="每行一段台词...

例如：
你今天看起来很开心。
我真的很难过。
不要生气，听我解释。
哇，太 surprise 了！" style="width:100%;height:100px;padding:10px;border:1px solid #d0d5dd;border-radius:8px;font-size:14px;font-family:inherit;resize:vertical;outline:none"></textarea>

<div style="margin:12px 0 8px 0"><strong style="font-size:14px">&#x1F3A4; 2. 上传音频</strong>
<div style="font-size:12px;color:#888">音频会被逐一识别情绪，与台词预期情绪对比。建议以序号开头对应台词行。</div></div>
<div class="upload-zone" id="analyzeAudioDropZone" style="padding:16px">
<div class="icon">&#x1F4C2;</div><div class="text">点击或拖放音频文件</div><div class="sub">WAV / MP3 / FLAC / M4A / AAC</div>
<input type="file" id="analyzeAudioInput" multiple accept=".wav,.mp3,.flac,.m4a,.aac,audio/*">
</div>
<div class="file-list" id="analyzeAudioList"></div>
</div>
<button class="btn btn-warning" id="analyzeBtn" disabled onclick="startAnalyze()">&#x1F916; AI 综合分析（需要 2+ 句台词和 2+ 个音频）</button>
<div class="batch-progress" id="analyzeProgress">
<div class="status-bar" style="margin:0"><span class="dot blue"></span><span id="analyzeProgressText">分析中...</span></div>
<div class="progress-wrap" style="margin:8px 0 0 0"><div class="progress-bar" id="analyzeProgressBar" style="width:0%"></div></div></div>
<div class="card" id="analyzeResult" style="display:none">
<div class="card-title">&#x1F9E0; AI 综合分析结果</div>
<div id="analyzeContent"></div>
<div class="btn-row"><button class="btn-outline" onclick="downloadAnalyzeReport()">&#x1F4E5; 导出报告</button></div>
</div></div>

<div class="footer">语音情绪识别系统 v2.0</div></div>

<script>
const ACCEPT=[".wav",".mp3",".flac",".m4a",".aac"];
let modelReady=false,batchFiles=[],batchResults=[],analyzeFiles=[],analyzeResults=[];

// 中文情绪映射
const CN={
  'neutral':'中性','calm':'平静','happy':'快乐','sad':'悲伤',
  'angry':'愤怒','fearful':'恐惧','disgust':'厌恶','surprised':'惊讶'
};
const EMOCN=t=>CN[t]||t;

async function pollStatus(){
try{
const r=await fetch("/api/status");const d=await r.json();
const dot=document.getElementById("statusDot"),txt=document.getElementById("statusText");
const pb=document.getElementById("progressBar"),pw=document.getElementById("progressWrap");
if(d.status==="ready"){
modelReady=true;dot.className="dot green";txt.textContent="就绪";
pb.className="progress-bar";pb.style.width="100%";
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
const pr=document.getElementById("predictBtn"),bt=document.getElementById("batchBtn"),az=document.getElementById("analyzeBtn");
if(!modelReady){
[pr,bt,az].forEach(b=>{b.textContent="模型加载中...";b.disabled=true;});return;
}
pr.textContent="&#x1F3A4; 识别情绪";pr.disabled=!document.getElementById("fileInput").files.length;
bt.textContent="&#x1F4CB; 批量识别";bt.disabled=batchFiles.length===0;
az.textContent="&#x1F916; AI 分析推荐";az.disabled=analyzeFiles.length<2;
}

function switchTab(name){
document.querySelectorAll(".tab").forEach(t=>t.classList.remove("active"));
document.querySelectorAll(".tab-content").forEach(t=>t.classList.remove("active"));
const idx={single:0,batch:1,analyze:2}[name]||0;
document.querySelectorAll(".tab")[idx].classList.add("active");
document.querySelectorAll(".tab-content")[idx].classList.add("active");
}

// === 单文件 ===
const dz=document.getElementById("dropZone"),fi=document.getElementById("fileInput");
dz.onclick=()=>fi.click();
dz.ondragover=e=>{e.preventDefault();dz.classList.add("dragover");};
dz.ondragleave=()=>dz.classList.remove("dragover");
dz.ondrop=e=>{e.preventDefault();dz.classList.remove("dragover");if(e.dataTransfer.files[0])handleSingle(e.dataTransfer.files[0]);};
fi.onchange=()=>{if(fi.files[0])handleSingle(fi.files[0]);};

function handleSingle(f){
const ext="."+f.name.split(".").pop().toLowerCase();
if(!ACCEPT.includes(ext)){alert("不支持: "+ext);return;}
document.getElementById("singleResult").style.display="none";updateButtons();
}

async function predict(){
if(!modelReady||!fi.files.length)return;
const btn=document.getElementById("predictBtn");btn.textContent="&#x23F3; 识别中...";btn.disabled=true;
const fd=new FormData();fd.append("audio",fi.files[0]);
try{
const r=await fetch("/api/predict",{method:"POST",body:fd});const d=await r.json();
if(d.error){alert("出错: "+d.error);return;}
showResult(d);
}catch(e){alert("失败: "+e.message);}
finally{updateButtons();}
}

function showResult(d){
document.getElementById("singleResult").style.display="block";
document.getElementById("resultEmotion").textContent=EMOCN(d.emotion)+"  ("+(d.confidence*100).toFixed(1)+"%)";
const colors=["#6366f1","#8b5cf6","#a855f7","#d946ef","#ec4899","#f43f5e","#ef4444","#f97316"];
let html='<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:8px">';
d.top_k.slice(0,5).forEach((item,i)=>{
const pct=(item.score*100).toFixed(1);
html+='<div style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:20px;background:'+colors[i%colors.length]+'20;border:1px solid '+colors[i%colors.length]+'40;font-size:13px">';
html+='<span style="font-weight:600;color:'+colors[i%colors.length]+'">'+EMOCN(item.label)+'</span>';
html+='<span style="color:#666;font-size:12px">'+pct+'%</span></div>';
});
html+='</div>';
document.getElementById("topkContainer").innerHTML=html;
}

// === 批量 ===
const bdz=document.getElementById("batchDropZone"),bfi=document.getElementById("batchFileInput");
bdz.onclick=()=>bfi.click();
bdz.ondragover=e=>{e.preventDefault();bdz.classList.add("dragover");};
bdz.ondragleave=()=>bdz.classList.remove("dragover");
bdz.ondrop=e=>{e.preventDefault();bdz.classList.remove("dragover");addBatch(e.dataTransfer.files);};
bfi.onchange=()=>{addBatch(bfi.files);bfi.value="";};

function addBatch(files){for(const f of files){const ext="."+f.name.split(".").pop().toLowerCase();if(ACCEPT.includes(ext))batchFiles.push(f);}renderBatch();updateButtons();}
function removeBatch(idx){batchFiles.splice(idx,1);renderBatch();updateButtons();}
function renderBatch(){
const el=document.getElementById("batchFileList");
if(batchFiles.length===0){el.innerHTML="";return;}
let h='<div style="font-size:13px;color:#888;margin-bottom:6px">共 '+batchFiles.length+' 个</div>';
batchFiles.forEach((f,i)=>{h+='<div class="file-item"><span class="name">'+f.name+' ('+(f.size/1024/1024).toFixed(1)+' MB)</span><span class="rm" onclick="removeBatch('+i+')">&#x2715;</span></div>';});
el.innerHTML=h;
}

async function batchPredict(){
if(!modelReady||batchFiles.length===0)return;
batchResults=[];document.getElementById("batchResult").style.display="none";
document.getElementById("batchProgress").classList.add("show");
const bar=document.getElementById("batchProgressBar"),txt=document.getElementById("batchProgressText");
document.getElementById("batchBtn").disabled=true;
for(let i=0;i<batchFiles.length;i++){
bar.style.width=((i)/batchFiles.length*100)+"%";txt.textContent="["+(i+1)+"/"+batchFiles.length+"] "+batchFiles[i].name;
const fd=new FormData();fd.append("audio",batchFiles[i]);
try{const r=await fetch("/api/predict",{method:"POST",body:fd});const d=await r.json();batchResults.push({file:batchFiles[i].name,result:d.error?{error:d.error}:d});}
catch(e){batchResults.push({file:batchFiles[i].name,result:{error:e.message}});}
}
bar.style.width="100%";txt.textContent="完成! 共 "+batchFiles.length+" 个";
document.getElementById("batchProgress").classList.remove("show");document.getElementById("batchResult").style.display="block";
const ok=batchResults.filter(r=>!r.result.error),er=batchResults.filter(r=>r.result.error);
document.getElementById("batchStats").textContent="成功 "+ok.length+" / 失败 "+er.length+" / 总计 "+batchResults.length;
const colors=["#6366f1","#8b5cf6","#a855f7","#d946ef","#ec4899","#f43f5e","#ef4444","#f97316"];
let h="";
batchResults.forEach((r,i)=>{
h+="<tr><td>"+(i+1)+"</td><td>"+r.file+"</td>";
if(r.result.error){h+='<td style="color:#ef4444">失败</td><td>-</td><td style="font-size:12px;color:#999">'+r.result.error+"</td>";}
else{const conf=(r.result.confidence*100).toFixed(1);const top=r.result.top_k||[];const detail=top.slice(0,3).map(t=>EMOCN(t.label)+" "+(t.score*100).toFixed(0)+"%").join(" | ");
h+='<td class="emo">'+EMOCN(r.result.emotion)+"</td>";
h+='<td><span class="bar-bg"><span class="bar-fill" style="width:'+conf+'%;background:'+colors[0]+'"></span></span><span class="pct">'+conf+"%</span></td>";
h+='<td style="font-size:12px;color:#888">'+detail+"</td>";}
h+="</tr>";});
document.getElementById("batchTbody").innerHTML=h;document.getElementById("batchBtn").disabled=false;updateButtons();
}


function downloadCSV(){
let rows=[];
rows.push([String.fromCharCode(65279)+"文件名","情绪","置信度","Top1","Top2","Top3"]);
batchResults.forEach(function(r){
var row;
if(r.result.error){
row=[r.file,"失败","-","-","-","-"];
}else{
var top=r.result.top_k||[];
var t1=top[0]?EMOCN(top[0].label)+" "+(top[0].score*100).toFixed(1)+"%":"-";
var t2=top[1]?EMOCN(top[1].label)+" "+(top[1].score*100).toFixed(1)+"%":"-";
var t3=top[2]?EMOCN(top[2].label)+" "+(top[2].score*100).toFixed(1)+"%":"-";
row=[r.file,EMOCN(r.result.emotion),(r.result.confidence*100).toFixed(1)+"%",t1,t2,t3];
}
rows.push(row);
});
var csvStr=rows.map(function(r){return r.join(",");}).join(String.fromCharCode(10));
var blob=new Blob([csvStr],{type:"text/csv;charset=utf-8"});
var url=URL.createObjectURL(blob);
var a=document.createElement("a");
a.href=url;a.download="emotion_results.csv";
a.click();
URL.revokeObjectURL(url);
}
// === AI 综合分析（文本预期 + 音频实际情绪匹配）===
var analyzeAudioFiles=[];
var EMOKEY2={
"快乐":["开心","高兴","快乐","哈哈","耶","好棒","太好了","喜欢","爱","幸福","微笑","笑","嘻嘻","乐","愉快","欢","爽","happy"],
"悲伤":["难过","伤心","悲伤","哭","泪","痛","失落","孤独","寂寞","悲","忧伤","sad","cry"],
"愤怒":["生气","愤怒","烦","讨厌","恨","气死","怒","恼火","暴躁","angry","furious"],
"恐惧":["害怕","恐惧","怕","慌","紧张","不安","心惊","吓","fear","scared"],
"惊讶":["惊讶","吃惊","震惊","哇","天啊","不是吧","竟然","居然","surprise","shock"],
"平静":["平静","放松","安静","淡定","从容","平和","calm","relax","peace"],
"中性":["嗯","哦","好的","可以","知道","明白","行","OK","neutral"],
"厌恶":["恶心","讨厌","反感","厌恶","disgust","gross"]
};
var emoIcon={"快乐":"😊","悲伤":"😢","愤怒":"😠","恐惧":"😨","惊讶":"😲","平静":"😌","中性":"😐","厌恶":"🤢"};

document.getElementById("analyzeAudioInput").onchange=function(){addAudioFiles(this.files);this.value="";};
var azDrop=document.getElementById("analyzeAudioDropZone");
azDrop.ondragover=function(e){e.preventDefault();this.classList.add("dragover");};
azDrop.ondragleave=function(){this.classList.remove("dragover");};
azDrop.ondrop=function(e){e.preventDefault();this.classList.remove("dragover");addAudioFiles(e.dataTransfer.files);};
azDrop.onclick=function(){document.getElementById("analyzeAudioInput").click();};

function addAudioFiles(files){for(var i=0;i<files.length;i++){var ext="."+files[i].name.split(".").pop().toLowerCase();if([".wav",".mp3",".flac",".m4a",".aac"].indexOf(ext)>=0)analyzeAudioFiles.push(files[i]);}renderAudioFiles();updateBtn2();}
function removeAudio(idx){analyzeAudioFiles.splice(idx,1);renderAudioFiles();updateBtn2();}
function renderAudioFiles(){var el=document.getElementById("analyzeAudioList");if(analyzeAudioFiles.length===0){el.innerHTML="";return;}var h="<div style=\"font-size:13px;color:#888;margin-bottom:6px\">共 "+analyzeAudioFiles.length+" 个音频</div>";for(var i=0;i<analyzeAudioFiles.length;i++)h+="<div class=\"file-item\"><span class=\"name\">"+analyzeAudioFiles[i].name+"</span><span class=\"rm\" onclick=\"removeAudio("+i+")\">&#x2715;</span></div>";el.innerHTML=h;}
function updateBtn2(){var n=document.getElementById("scriptInput").value.trim().split("\\n").filter(function(l){return l.trim();}).length;var b=document.getElementById("analyzeBtn");if(n>=2&&analyzeAudioFiles.length>=2){b.disabled=false;b.innerHTML="&#x1F916; AI 综合分析";}else{b.disabled=true;b.innerHTML="&#x23F3; 需要 2+ 句台词和 2+ 个音频";}}
document.getElementById("scriptInput").oninput=updateBtn2;

async function startAnalyze(){
var text=document.getElementById("scriptInput").value.trim();
var lines=text.split("\\n").filter(function(l){return l.trim();});
if(text.trim().length<1||analyzeAudioFiles.length<2){alert("至少需要 1 句台词和 2 个音频");return;}
document.getElementById("analyzeResult").style.display="none";
document.getElementById("analyzeProgress").classList.add("show");
var bar=document.getElementById("analyzeProgressBar"),txt=document.getElementById("analyzeProgressText");
document.getElementById("analyzeBtn").disabled=true;

// 1. 文本预期情绪分析（整段文本）
var textEmo="中性",tmpSc={};for(var e in EMOKEY2){tmpSc[e]=0;}
var tmpTot=0;
for(var e in EMOKEY2){EMOKEY2[e].forEach(function(kw){var r=new RegExp(kw,"gi");var m=text.match(r);if(m){tmpSc[e]+=m.length;tmpTot+=m.length;}});}
var ts2=0;for(var e in tmpSc){if(tmpSc[e]>ts2){textEmo=e;ts2=tmpSc[e];}}

// 2. 音频情绪识别
var audioR=[];
for(var i=0;i<analyzeAudioFiles.length;i++){
bar.style.width=((i+1)/analyzeAudioFiles.length*100)+"%";
txt.textContent="识别 ["+(i+1)+"/"+analyzeAudioFiles.length+"] "+analyzeAudioFiles[i].name;
var fd=new FormData();fd.append("audio",analyzeAudioFiles[i]);
try{
var r=await fetch("/api/predict",{method:"POST",body:fd});var d=await r.json();
audioR.push({file:analyzeAudioFiles[i].name,emo:d.emotion,conf:d.confidence,err:null});
}catch(e){audioR.push({file:analyzeAudioFiles[i].name,emo:"error",conf:0,err:e.message});}
}

// 3. 匹配：所有音频与同一段文本对比
var all=[];
for(var i=0;i<audioR.length;i++){
var a=audioR[i];if(a.err){all.push({file:a.file,err:a.err,score:0});continue;}
var s=0;
s=(a.emo===textEmo?100:(a.emo==="neutral"&&textEmo==="平静")||(a.emo==="平静"&&textEmo==="neutral")?85:40);
s=s*0.6+a.conf*0.4*100;if(a.emo==="愤怒"||a.emo==="恐惧")s*=0.85;
s=Math.round(s);
all.push({file:a.file,audioEmo:a.emo,audioConf:a.conf,text:text,expectEmo:textEmo,score:s,err:null});
}
all.sort(function(a,b){return b.score-a.score;});

var colors=["#22c55e","#f59e0b","#ef4444"];
var html="<div style=\"margin-bottom:12px;font-size:13px;color:#888\">共识别 "+audioR.length+" 条，匹配度越高越适合作参考</div>";
for(var i=0;i<all.length;i++){
var r=all[i];
if(r.err){html+="<div class=\"rank-card\"><div style=\"color:#ef4444\">&#x274C; "+r.file+" - "+r.err+"</div></div>";continue;}
var badge=i===0?"&#x1F947; 主参考":i===1?"&#x1F948; 副参考":"&#x1F4AD; 备选";
var bc=i===0?"gold":i===1?"silver":"";
var cc=i===0?'class="rank-card top1"':i===1?'class="rank-card top2"':'class="rank-card"';
var sc=r.score>=80?colors[0]:r.score>=60?colors[1]:colors[2];
html+="<div "+cc+"><div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap\"><span class=\"rank-badge "+bc+"\">"+badge+"</span><strong>"+r.file+"</strong></div>";
html+="<div class=\"ai-score\" style=\"margin-top:8px\">";
html+="<div class=\"ai-score-item\"><div class=\"ai-score-val\" style=\"color:"+sc+"\">"+r.score+"</div><div class=\"ai-score-label\">匹配度</div></div>";
html+="<div class=\"ai-score-item\"><div class=\"ai-score-val\">"+(emoIcon[r.audioEmo]||"")+" "+r.audioEmo+"</div><div class=\"ai-score-label\">实际情绪</div></div>";
html+="<div class=\"ai-score-item\"><div class=\"ai-score-val\" style=\"font-size:16px\">"+(r.audioConf*100).toFixed(0)+"%</div><div class=\"ai-score-label\">置信度</div></div>";
html+="<div class=\"ai-score-item\"><div class=\"ai-score-val\" style=\"font-size:16px\">&#x1F4DD; "+r.expectEmo+"</div><div class=\"ai-score-label\">预期情绪</div></div>";
html+="<div style=\"flex:1;min-width:80px\"><div class=\"ai-score-label\">匹配度</div><div style=\"height:8px;background:#e5e7eb;border-radius:4px;overflow:hidden\"><div style=\"height:100%;width:"+r.score+"%;background:"+sc+";border-radius:4px\"></div></div></div></div>";
var reason=r.audioEmo===r.expectEmo?"实际表达与预期一致。":"实际表达（"+r.audioEmo+"）与预期（"+r.expectEmo+"）有差异。";
if(r.score>=85)reason="高度匹配，非常适合做参考音频。";
html+="<div class=\"ai-reason\" style=\"margin-top:6px;font-size:12px\">对应: &quot;"+(r.text.length>45?r.text.slice(0,45)+"...":r.text)+"&quot;<br>"+reason+"</div></div>";
}
html+="<div style=\"margin-top:12px;padding:10px;background:#f8f9ff;border-radius:8px;font-size:12px;color:#666\">";
html+="<strong>说明：</strong>匹配度 = 音频实际情绪与文本预期情绪的接近程度 + 置信度加权。匹配度越高越适合做参考音频。</div>";
document.getElementById("analyzeContent").innerHTML=html;
document.getElementById("analyzeResult").style.display="block";
bar.style.width="100%";txt.textContent="完成!";
document.getElementById("analyzeProgress").classList.remove("show");
document.getElementById("analyzeBtn").disabled=false;
}

function downloadAnalyzeReport(){
var d=new Date();
var report="AI 综合分析报告\\r\\n生成时间: "+d.toLocaleString();
report+="\\r\\n==================================================\\r\\n\\r\\n";
report+="【输入文本】\\r\\n"+document.getElementById("scriptInput").value.trim()+"\\r\\n\\r\\n";
report+="【分析结果】请从页面查看。\\r\\n";
var blob=new Blob([report],{type:"text/plain;charset=utf-8"});
var url=URL.createObjectURL(blob);var a=document.createElement("a");a.href=url;a.download="analyze_report.txt";a.click();URL.revokeObjectURL(url);
}
</script>
</body>
</html>
"""

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


@app.route("/favicon.ico")
def favicon():
    return "", 204


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
