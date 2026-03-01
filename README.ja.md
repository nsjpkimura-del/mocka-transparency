\# MoCKA Transparency v2



English version: README.md



---



\## 3分で体験する Transparency デモ（Sample01）



このデモでは「改ざん検出」を体験できます。



流れ：



1\. 正常状態を検証する（PASS）

2\. ファイルを改ざんする

3\. 検証が FAIL することを確認する

4\. 元に戻して再検証する（PASS）



---



\### 1. クローン



git clone https://github.com/nsjpkimura-del/mocka-transparency.git

cd mocka-transparency



---



\### 2. 検証（PASS になる）



powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verify\_one.ps1



表示例：

PASS: Sample01 verified



---



\### 3. 改ざんデモ（FAIL になる）



powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\tamper\_demo.ps1



表示例：

FAIL: decision\_log.json sha256 mismatch



---



\### 4. 復旧（再び PASS）



git restore .\\sample01\\decision\_log.json

powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verify\_one.ps1



---



このデモで分かること：



・署名されたログは改ざんできない  

・改ざんすると即座に検出される  

・公開鍵のみで検証できる  

・Git により確実に復旧できる

