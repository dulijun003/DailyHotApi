# Mindustry 运行教程

Mindustry 是一款开源的「自动化 + 塔防 + 即时战略」游戏（GitHub：Anuken/Mindustry，约 2.9 万星，GPL-3.0 许可证）。

`demo.mp4` 是在云端机器上从源码编译、实际运行并录下来的画面（第一关 Ground Zero 的新手教程，约 90 秒，已加速、无声音）。

---

## 方式一：直接下载玩（最简单，推荐）

| 设备 | 去哪里下载 |
|---|---|
| Windows / Mac / Linux | GitHub 的 Releases 页面：<https://github.com/Anuken/Mindustry/releases>，下载 `Mindustry.jar`（需要先装 Java 17 或更高版本）；或者在 itch.io 搜 Mindustry 下载对应系统的安装包 |
| 安卓手机 | Google Play、F-Droid 搜「Mindustry」，或者在 GitHub Releases 页面下载 `.apk` 安装 |
| 苹果手机 | App Store 搜「Mindustry」（付费） |
| Steam | 搜「Mindustry」（付费，和免费版内容一样，多了 Steam 联机和创意工坊） |

### 运行 jar 文件的步骤（电脑）

1. 安装 Java 17 或更高版本（推荐 Eclipse Temurin：<https://adoptium.net>，选 JDK 21 下载安装）。
2. 打开终端（Windows 用「命令提示符」或 PowerShell，Mac 用「终端」），检查是否装好：
   ```
   java -version
   ```
   显示 `17` 或更高的版本号就行。
3. 进入 `Mindustry.jar` 所在的文件夹，运行：
   ```
   java -jar Mindustry.jar
   ```
   大多数电脑上直接双击 `Mindustry.jar` 也能打开。

---

## 方式二：从源码自己编译（想改游戏的话用这个）

需要：Git、Java 17 或更高版本。

```bash
# 1. 把游戏和它的引擎 Arc 下载到同一个文件夹里（两个文件夹并排放）
git clone --depth 1 https://github.com/Anuken/Mindustry
git clone --depth 1 https://github.com/Anuken/Arc

# 2. 进入游戏目录，直接编译并启动
cd Mindustry
./gradlew desktop:run          # Windows 上用：gradlew.bat desktop:run

# 3. 或者打包成一个 jar 文件（生成在 desktop/build/libs/Mindustry.jar）
./gradlew desktop:dist
```

第一次编译会自动下载 Gradle 和依赖，需要几分钟。

如果编译时提示连不上 jitpack.io（国内网络常见），把下面两个仓库也下载到同一个文件夹，并在 `Mindustry` 目录里新建 `local.properties` 文件：

```bash
git clone --depth 1 https://github.com/Anuken/rhino
git clone --depth 1 https://github.com/Anuken/steamworks4j
```

`local.properties` 内容：
```
localRhino=true
localSteamworks=true
```

我在云端就是这样编译成功的（文件夹结构：`Arc/  Mindustry/  rhino/  steamworks4j/` 四个并排）。

---

## 新手怎么玩（第一关 Ground Zero）

1. 主菜单 → **Play** → **Campaign** → 选紫色星球 **Serpulo** → **OK** → 选中 **Ground Zero** → **Launch**。
2. **手动挖矿**：点地上的铜矿（橙色小石块），你的小飞机会自动去挖。
3. **研究钻头**：点右下角的「科技树」图标（像三叉的那个）→ 点 **机械钻头 (Mechanical Drill)** 研究 → **Back** 返回。
4. **放钻头**：右下角建筑栏里选钻头，点在铜矿上，钻头会自动采矿。
5. **研究传送带**：再进科技树，找到 **传送带 (Conveyor)**（在核心节点左边的分支），点它研究。
6. **铺传送带**：建筑栏右侧切到「运输」分类，选传送带，**按住鼠标拖动**，从钻头旁边拉到核心（中间那个大方块）。资源就会沿着传送带自动运进核心。
7. 之后按教程提示：建炮塔防守敌人波次、研究更多建筑，搭建越来越复杂的自动化生产线。

### 常用操作（电脑）

| 操作 | 按键 |
|---|---|
| 移动视角 | W A S D |
| 缩放 | 鼠标滚轮 |
| 放置建筑 | 左键（拖动可以连续放） |
| 旋转建筑方向 | 放置前滚动鼠标滚轮 |
| 取消选择 / 拆除 | 右键 |
| 暂停 | 空格 |

手机版是触屏操作：点选建筑后点地图放置，双指缩放。

游戏支持中文：主菜单 → **Settings** → **Language** 选「简体中文」。
