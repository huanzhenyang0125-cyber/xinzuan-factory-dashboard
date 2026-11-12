# 新钻经营看板

全中文经营概览、采购分析、预算测算与年度台账。

- 在线版：GitHub Pages，支持手机和电脑。
- 浏览器交互：菜单收缩、年份切换、滑块与数值输入、原值和测算值柱状图。
- Python 版：安装 `requirements.txt` 后运行 `streamlit run app.py`。

金额单位为人民币。数据为提供的 2020—2026 年度汇总，空白保留为未记录，采购合计仅汇总已录入项目。质量预测页面等待生产批次数据接入。

中文字体为霞鹜新晰黑，许可见 `assets/FONT-LICENSE.md`。

页面使用重命名为 CompanyText 的字体子集。原始字体位于 `assets/original/LXGWNeoXiHei.ttf`；如需替换为原字体，将样式表的 `@font-face` 地址改为该文件并使用 `format('truetype')` 即可。子集生成方法见 `font-subset.py`，原项目为 https://github.com/lxgw/LxgwNeoXiHei 。
