# 公众号排版（article.wechat.html）

公众号编辑器会过滤 `<style>`、`<script>` 和 class，**所有样式都必须写成内联 `style`**。生成的 HTML 用浏览器打开后，全选复制，再粘贴到公众号编辑器即可。

## 规则

- 只使用这些标签：`section`、`p`、`h2`、`h3`、`strong`、`em`、`span`、`blockquote`、`ul`、`ol`、`li`、`img`、`br`、`hr`、`sup`
- 不要使用 `class`、`id`、外部 CSS、`position`、`float` 和 JavaScript
- 链接在公众号正文中不可点击，所以参考资料要写出完整网址（纯文本）
- 配图位置用占位块，提示用户在编辑器里替换成上传的图片
- 脚注改写为上标 `<sup>[3]</sup>`，文末列出参考资料

## 默认样式（可按用户偏好调整主色）

主色 `#2B6CB0`（蓝），正文色 `#333`，辅助色 `#888`，字号 15px，行高 1.8。

```html
<section style="font-size:15px;line-height:1.8;color:#333;letter-spacing:0.5px;padding:0 4px;">

  <!-- 导语 -->
  <section style="background:#F5F8FC;border-left:4px solid #2B6CB0;padding:12px 16px;margin:0 0 24px;color:#555;font-size:14px;">
    导语/摘要文字
  </section>

  <!-- 二级标题 -->
  <h2 style="font-size:18px;font-weight:bold;color:#2B6CB0;border-bottom:2px solid #2B6CB0;padding-bottom:6px;margin:32px 0 16px;">01 小标题</h2>

  <!-- 三级标题 -->
  <h3 style="font-size:16px;font-weight:bold;color:#333;margin:24px 0 12px;">▍三级标题</h3>

  <!-- 段落 -->
  <p style="margin:0 0 16px;text-align:justify;">正文段落，关键句<strong style="color:#2B6CB0;">加粗强调</strong>。<sup style="color:#888;font-size:11px;">[3]</sup></p>

  <!-- 引用/金句 -->
  <blockquote style="margin:20px 0;padding:12px 16px;background:#FAFAFA;border-left:3px solid #CCC;color:#666;font-size:14px;">引用内容</blockquote>

  <!-- 图片占位 -->
  <section style="margin:20px 0;padding:40px 0;background:#EEF2F7;text-align:center;color:#999;font-size:13px;">【此处插入 图1：说明】</section>
  <p style="text-align:center;color:#999;font-size:12px;margin:-12px 0 20px;">图1：图片说明 ｜ 来源：……</p>

  <!-- 参考资料 -->
  <h2 style="...同上...">参考资料</h2>
  <p style="font-size:12px;color:#888;line-height:1.6;margin:0 0 6px;word-break:break-all;">[1] 作者.《标题》. 出处, 日期. https://…</p>

</section>
```

## 节奏建议

- 正文每 2–3 屏要有一个视觉"停顿点"，比如小标题、配图、金句引用或数据卡片
- 每节最多 1–2 处加粗，只用在真正的核心句上
- 二级标题加上编号（01/02/03），方便读者知道自己读到了哪里
