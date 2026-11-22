# 路线地图页制作（腾讯地图 JS API GL）

## 何时需要

方案中有多条可选路线、地点分散时，做一个独立的可交互地图页，并在方案里放链接与截图。
地图页需联网（加载腾讯地图 API 与底图），方案主文件仍保持离线自包含。

## 页面骨架

```
<div class="hd">标题/说明</div>
<div class="bar"><button id="b-all">全部地点</button><button id="b-d1">首日下午</button>...</div>
<div id="map"></div>
<div class="legend">图例与行程顺序</div>
<div class="tip">操作提示</div>
<script src="https://map.qq.com/api/gljs?v=1.exp&key=<KEY>"></script>
<script>
  const P = { ...地点表... };      // 坐标 GCJ-02
  const COLORS = {...};
  const routes = {...};            // MultiPolyline 路线
  const VIEWS = {...};             // 每个按钮的 center/zoom/显示哪些路线
  function show(key){...}          // 切换线路：设中心/缩放、过滤路线与标记
</script>
```

## 地点表 P

每项：`{name, short, lat, lng, g(颜色组), d(说明)}`。
- `short` 是地图上的标签文字。方案图例、截图、在线地图三处的**编号与名称必须一致**。
- 编号用简单数字（`1 海尚酒店`），不要用圈号 ①——圈号在不同字体下大小不一致。
- 坐标用腾讯地图口径 GCJ-02，可用 WebSearch 查"地点名 经纬度 腾讯地图"获得。

## 路线连线

用 `TMap.MultiPolyline`，样式要点：
- **实线**（游玩路线）：`new TMap.PolylineStyle({color,width:5,borderWidth:1,borderColor:'#fff',lineCap:'round'})`
- **虚线**（坐车转场）：同样参数加 `dashArray:[6,6]`（正确属性是 `dashArray`，不是 `lineSpace.dashArray`）。
- 一条路线若含多种性质（如"酒店→景点坐车 + 景点间游玩"），拆成两条 Polyline：虚线段 + 实线段。

## 底图要素

隐藏底图自带地名，避免与自定义标签叠加：

```js
map.setBaseMap({type:'vector', features:['base','building3d','arrow']});
```

去掉 `label`/`point` 即可隐藏所有 POI 文字与图标，只留道路/建筑/方向。

## 视图切换 show()

- 用 `setCenter` + `setZoom` 切换视角。
- 用 `setMap(map|null)` 控制每条路线显隐。
- 标记与标签用 `getGeometries()` 过滤后 `setGeometries()` 更新。
- 可选点按归属分配到不同视图（如南头古城归 A 线、深业上城归 B 线）。

## 截图嵌入方案

地图页做好后，截图放到方案的 `routemap` 章节。截图步骤（Chrome DevTools）：
1. 设视口约 1200×560。
2. 用 evaluate 隐藏 `.hd`/`.bar`/`.legend`/`.tip`，把 `#map` 高度设为视口高。
3. 设中心与缩放到能容纳所有点，调用 `show('all')`。
4. **把标签内容改成纯数字**（如 `1`–`13`）：全览缩放下"数字+全称"会严重重叠，纯编号清晰；名称放在方案的 `.maplegend` 里对照。
5. 截图后转成 WebP 并以 data URI 内嵌进方案。

## 三处一致性检查

| 位置 | 内容 |
|---|---|
| 方案图例 `.maplegend` | 编号 1–13 + 名称（含"可选"标注） |
| 方案内截图 | 纯数字 1–13 + 路线连线 |
| 在线地图 | short 标签 `1 名称`、图例 HTML |

改动编号/名称时三处同步改，并在方案说明里写明"图中编号与图例、在线地图一致"。
