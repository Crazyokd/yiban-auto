# yiban-auto
csust易班校本化自动健康打卡.【[English](README_en.md)】

## 目录
- [免责声明](#免责声明)
- [用法](#用法)
- [参考](#参考)
- [协议](#协议)

## 免责声明
- 本项目涉及的任何脚本，仅供学习测试研究，禁止用于商业用途。
- 使用本项目时，需先遵守法律法规。使用过程中照成的任何后果，需自行承担，对于任何关于本项目的问题概不负责，包括使用过程中导致的任何损失和损害。
- 如果出现发热、干咳、体寒、身体不适、胸痛、鼻塞、流鼻涕、恶心、腹泻等症状。请立即停止使用本项目，认真履行社会义务，及时进行健康申报。
- 如有侵权，请提供相关证明，所有权证明，本人收到后删除相关文件。
- 无论以任何方式查看、复制或使用到本项目中的任何脚本，都应该仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。
- 一旦使用并复制了本项目的任何相关脚本，则默认视为您已经接受了此免责声明。
## 用法
### 1. 安装依赖
```python
pip install -r requirements.txt
```
### 2. 填写信息
- 1. 编辑[address.json](address.json)文件
- 2. 运行下面的程序从而得到您详细的地址信息。 
    ```python
    python getaddress.py
    ```
- 3. 编辑[config.json](config.json)文件
### 3. 运行程序
```python
python main.py
```
## 参考
- [Sricor/Yiban](https://github.com/Sricor/Yiban)
- [apecodex/yibanAutoSgin](https://github.com/apecodex/yibanAutoSgin)

## 协议
在**Apache-2.0**许可证下发布。有关更多信息，请参阅[LICENSE](LICENSE)。
