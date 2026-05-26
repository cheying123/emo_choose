"""
语音情绪识别系统快速启动脚本
基于 HuggingFace 预训练模型，即开即用
"""
import os
import sys


def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 60)
    print("           语音情绪识别系统 v2.0 - 快速开始")
    print("          基于 HuggingFace 预训练模型，即开即用")
    print("=" * 60)
    print("请选择要执行的操作：")
    print("1. 启动图形界面")
    print("2. 批量处理音频文件")
    print("3. 查看系统信息")
    print("4. 运行演示程序")
    print("5. 创建示例数据集目录结构")
    print("6. 退出")
    print("=" * 60)


def launch_gui():
    """启动图形界面"""
    print("\n正在启动图形界面...")
    try:
        from gui_app import main as gui_main
        gui_main()
    except Exception as e:
        print(f"启动失败: {e}")


def batch_process():
    """批量处理音频文件"""
    folder = input("\n请输入音频文件夹路径: ").strip()
    if not folder:
        print("已取消")
        return
    if not os.path.exists(folder):
        print(f"文件夹不存在: {folder}")
        return

    try:
        from batch_process import batch_predict_from_folder
        output = f"emotion_results_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        batch_predict_from_folder(folder, output)
    except Exception as e:
        print(f"处理失败: {e}")


def show_system_info():
    """显示系统信息"""
    print("\n" + "=" * 50)
    print("           系统信息")
    print("=" * 50)
    print("语音情绪识别系统 v2.0")
    print()
    print("核心特性:")
    print("  • 基于 HuggingFace 预训练模型")
    print("  • 支持多语种（中文、粤语、英语、日语等）")
    print("  • 即开即用，无需训练")
    print("  • 支持 8 种情绪识别")
    print()
    print("支持的情绪:")
    print("  中性(neutral)、平静(calm)、快乐(happy)、悲伤(sad)")
    print("  愤怒(angry)、恐惧(fearful)、厌恶(disgust)、惊讶(surprised)")
    print()
    print("支持的音频格式: WAV, MP3, FLAC, M4A, AAC")
    print()
    print("使用方式:")
    print("  1. python gui_app.py          # 图形界面")
    print("  2. python batch_process.py ... # 命令行批量处理")
    print("  3. python demo.py             # 演示")
    print("=" * 50)


def run_demo():
    """运行演示程序"""
    print("\n正在运行演示程序...")
    try:
        from demo import main as demo_main
        demo_main()
    except Exception as e:
        print(f"演示程序运行出错: {e}")


def create_sample_dataset():
    """创建示例数据集目录结构"""
    from batch_process import create_sample_dataset_structure
    create_sample_dataset_structure()


def main():
    """主函数"""
    print("欢迎使用语音情绪识别系统 v2.0！")
    print("首次使用需要下载模型（约 1.5GB），请确保网络畅通。")

    while True:
        show_menu()
        choice = input("\n请输入选项编号 (1-6): ").strip()

        actions = {
            "1": launch_gui,
            "2": batch_process,
            "3": show_system_info,
            "4": run_demo,
            "5": create_sample_dataset,
        }

        if choice == "6":
            print("\n感谢使用！再见！")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("\n无效选项，请重新选择。")

        if choice != "1":  # GUI 自己管理事件循环，不需要 pause
            input("\n按回车键继续...")


if __name__ == "__main__":
    main()
