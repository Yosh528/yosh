#!/usr/bin/env python3
"""
Novel-to-Script CLI 主程序
Usage: python main.py --input <novel.txt> --output <script.yaml> [--chapter-num N]
"""
import argparse
import sys
from pathlib import Path
from src.validators.yaml_validator import ScreenplayValidator
from src.utils.fountain import FountainConverter


def main():
    parser = argparse.ArgumentParser(
        description="AI 小说转剧本工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py -i novel.txt -o script.yaml
  python main.py -i novel.txt -o script.yaml -n 1 --to-fountain
  python main.py -i novel.txt -o script.yaml --validate
        """
    )
    parser.add_argument("--input", "-i", required=True, help="输入小说文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出 YAML 文件路径")
    parser.add_argument("--chapter-num", "-n", type=int, default=1, help="章节编号")
    parser.add_argument("--prev-yaml", "-p", help="前序章节 YAML 路径 (用于角色一致性)")
    parser.add_argument("--to-fountain", "-f", action="store_true", help="同时输出 Fountain 文件")
    parser.add_argument("--validate", "-v", action="store_true", help="输出后执行校验")
    parser.add_argument("--strict", "-s", action="store_true", default=False, help="严格模式校验")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {args.input}")
        sys.exit(1)

    # 读取小说文本
    with open(input_path, 'r', encoding='utf-8') as f:
        novel_text = f.read()

    print(f"已读取小说文本: {len(novel_text)} 字符")
    print(f"章节编号: {args.chapter_num}")
    print()
    print("=" * 50)
    print("下一步操作:")
    print("1. 将小说文本和 system-prompt.txt 一起提交给 AI 模型")
    print("2. AI 将返回 YAML 格式的剧本")
    print("3. 保存 YAML 到:", args.output)
    print()

    if args.validate:
        validator = ScreenplayValidator(strict=args.strict)
        valid, errors = validator.validate_file(args.output)
        if not valid:
            print("校验失败:")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)
        print("✓ 校验通过")

    if args.to_fountain:
        from src.utils.fountain import convert_to_fountain
        result = convert_to_fountain(args.output)
        print(f"✓ 已转换为 Fountain 格式")


if __name__ == "__main__":
    main()