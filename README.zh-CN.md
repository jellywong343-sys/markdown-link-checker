# Markdown 閾炬帴妫€鏌ュ伐鍏?
[English](README.md)

妫€鏌?Markdown 鏂囨。涓殑鏈湴澶辨晥閾炬帴銆侀噸澶嶇洰鏍囧拰鍙€夌殑澶栭儴缃戦〉閿欒銆?
## 鍔熻兘鐗圭偣

- 鏈湴鏂囦欢妫€鏌ヤ笉闇€瑕佺綉缁溿€?- 鍙湁浣跨敤 `--external` 鎵嶄細璁块棶澶栭儴缃戝潃銆?- 鏄剧ず鍑嗙‘鐨勬枃浠跺悕鍜岃鍙枫€?- 鏀寔瀵煎嚭 JSON锛屼究浜庢枃妗ｆ祦绋嬪拰鎸佺画闆嗘垚浣跨敤銆?- 涓嶄細淇敼鍘?Markdown 鏂囦欢銆?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/markdown-link-checker.git
cd markdown-link-checker
python -m pip install -e .
```

## 浣跨敤

```bash
md-link-check README.md
md-link-check README.md docs/index.md --json links.json
md-link-check README.md --external --timeout 5
```

澶栭儴妫€鏌ヤ細鍚戞枃妗ｄ腑鐨勭綉鍧€鍙戦€佺綉缁滆姹傦紝鍥犳榛樿鍏抽棴銆?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT



