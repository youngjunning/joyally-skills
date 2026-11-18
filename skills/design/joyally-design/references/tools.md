# 工具

本目录自带的程序不需要读源码，命令里的 `<skill>` 换成本 Skill 的安装目录。这里只写什么时候用和最常用的几条命令；全部选项、动作写法和输出文件见各自的 `--help`，写错时报错会给出照抄就能用的写法。

需要生成文件时，先按 [任务工作区](workdir.md) 确定过程输出和各工具的命令目录。没有项目约定时用 `.joyally-design/<任务名>`；显式输出路径始终优先，截图和正式图片处理还有各自的 cwd 要求。

任务已指定截图工具时照用；宿主提供下节列出的专用工具时用宿主的。其余情况用 `shoot.mjs` 取证：它起一个独立的临时浏览器，不碰用户的浏览器数据，并且带可读性检查，环境里的通用浏览器工具替代不了这一步。点击、填写、提交和刷新读回已经由 `--steps` 走过的，不再开第二个浏览器重跑；只有 `--steps` 表达不了的连续交互才加用通用浏览器。缺 Node 22 或没有可用的 Chrome、Chromium、Edge 时，再退回通用浏览器截图。

## 宿主工具

宿主自带截图、素材检索或对比页工具时，可按任务使用并遵循它的参数说明。需要生成或编辑图片时，按[生图设计与还原校准](image-ideation.md)调用 `joyally-image`；模型和服务状态以该生图流程的实际检查结果为准。

## 截图和录屏

### 什么时候截，截多少

截图分两种用途，不要混在一起：

- **看一眼**：改完一批，想看效果。只截当前这一屏，一条命令。把一批改动攒在一起改完再截，不是每改一处截一次；页面没有变，就不重复截。
- **取证**：送评审或交付前保留标准视口图。跨设备响应式任务用 `--size desktop,mobile`（1440×900、390×844）；明确只做手机或桌面时只取那一端。按需带一两个代表交互态，用 `--steps` 走真实操作；页面本来就读查询参数时才用 `--states`，不为截图给页面加 `?state=` 路由。长页才加 `--full`（`fullPage: true`）；页面不适合截整页时工具会提示，照提示改截视口。比较状态加 `--sheet`，遮字加 `--mask`；方向预览每个只截首屏。

动效默认用 `--frames` 生成带时间的序列图，或让评审者打开页面直接操作。只有确实要判断正常速度下的手感、且评审能播放视频时才用 `--record`，不为交付而录屏。确实需要整套证据时用 `--evidence --frames <帧数>`；满足上述录屏条件才加 `--record`。

每一轮评审只重新取这一轮改动影响到的证据。没有动过的状态和动效，沿用上一轮的文件，交接时注明哪些是沿用的；拿不准有没有被影响到，例如改了共享样式，就重取那一项。评审者只提出扩大覆盖、却说不清哪条判断缺少依据时，不补图也不加一轮。

### 常用命令

跨端响应式页面：

```text
node <skill>/scripts/shoot.mjs index.html --size desktop,mobile --out shots
```

| 要什么 | 加上 |
| --- | --- |
| 按任务设备取标准视口 | 跨端用 `index.html --size desktop,mobile --out shots`；单端用 `--size mobile` 或 `--size desktop`（省略尺寸默认手机；只看整体可加 `--thumb`） |
| 一次截完多个候选并出并排图 | 直接传候选目录（如 `explore`）或多个 HTML 文件，同一次浏览器会话截完并自动出 `sheet.png` |
| 只看改过的局部组件或区域 | `--selector ".card"`，自动滚入视口并只截该元素区域 |
| 页面本来就用 URL 参数切视图 | `index.html --param tab --states queue,points --out shots`，如 `?tab=points` |
| 一次取多个交互态并命名 | `--steps "open: click .open" --steps "submit: click .open; fill #name 内容; click .submit" --out shots`；各组重新打开页面，组内写全入口步骤 |
| 需要核对长页滚动动效 | `--frames 8 --steps "scroll 600; scroll 600; scroll 600"`，按页面长度多写几步；录屏条件见上文 |
| 给用户指出问题：在元素上画框、标编号 | `--mark "1=.page-head .btn; 2=.toggle-row"` |
| 交付时启用三级质量门禁 | `--gates`；未解释的 Floor 或 Reflex 返回 1，规则与例外格式见[三级质量门禁](quality-gates.md) |
| 重设计前记录并核对存量接线 | 修改前 `--before .joyally-design/page-before.json`，修改后 `--kept .joyally-design/page-before.json --gates` |
| 核对真实素材来源、许可、用途与页面接线 | `--materials materials.json --gates`；HTML 用 `data-joyally-material` 关联稳定 ID，格式见[真实素材清单](quality-gates.md#第二期真实素材清单) |
| 看清一段过渡 | `--frames 8 --steps "click .open"`，只出带时间的序列图；录屏条件见上文 |
| 把几张图拼成一张对比图，不需要页面 | `--stitch a.png --label 修改前 --stitch b.png --label 修改后` |
| 按共有元素统一比例并裁同一区域 | `--stitch a.png --match-width 240 --stitch b.png --match-width 300 --crop "0,0,800,600"`；以首图元素宽为准，裁切坐标在统一比例后；已知倍数时各图改用 `--scale`，完整写法见 `--help` |

用真实视图或命名动作组合批，生成具名 PNG 和一份 `report.json`，避免分次输出的 `index-2.png` 等编号碰撞，不另写报告合并脚本；两者合用时，每个视图都会执行每组动作。

交互从真实入口走到结果：保存后刷新或重新进入读回，失败后恢复到可重试状态；留对应截图或操作记录，不能执行就写明未验证，浏览器分工沿用开头。完整动作与输出见 `node <skill>/scripts/shoot.mjs --help`；拿不准先加 `--dry-run`，不启动浏览器。超时自动放宽时限重跑一次，仍失败按报错命令重跑。

本地相对路径和 `file:///` 地址都保留查询参数与锚点，例如 `"index.html?season=summer#top" --query "lang=zh" --states idle,done`。文件解析、`--root` 边界检查与输出文件名只使用纯路径。合并时先保留地址参数，再由 `--query` 覆盖同名参数（重复值全部保留），最后由 `--states` 覆盖状态参数；其他参数与锚点保留。地址含 `?`、`&` 或 `#` 时给整个地址加引号。

### 检索和下载真实素材

在项目工作目录运行，后续命令也在同一目录，搜索结果的编号才接得上：

```text
node <skill>/scripts/curate-media.mjs search "<关键词>" --kind texture --limit 6 --sheet --dir candidates
node <skill>/scripts/curate-media.mjs search "<一组词> | <另一组词>" --sheet --dir candidates
node <skill>/scripts/curate-media.mjs preview V1,T2 --sheet --dir candidates
node <skill>/scripts/curate-media.mjs fetch C1,T2 --dir assets --sheet
node <skill>/scripts/curate-media.mjs fetch V3 --dir <不上线的参考图目录>
node <skill>/scripts/curate-media.mjs fetch T2 --maps all --resolution 1k --dir assets
```

`--kind` 支持 `all|texture|design|photo|blueprint|map|plate|science|video`。信源包括材质库、欧美与日本的博物馆和图书馆馆藏、NASA，各类别对应哪些信源见 `--help`。`all` 交错取各信源；用 `|` 可一次搜几组词。关键词多用英文，东亚题材可直接用中日文，简体搜不到时换繁体或日文写法。

结果存入 `.curate-cache.json`，编号跨次搜索保留。每项 `use` 说明用途：`page` 可放进页面（CC BY/BY-SA 要署名），`check` 先看来源页，`reference` 不能放进页面；`--use page` 只留第一种。

`search --sheet` 和 `preview` 出带编号、用途和原图尺寸的联系表 PNG，直接读这张图挑选，不要只看标题；同时给每项算 `look`（四边色、是否浅色纸底、哪些区域干净可压字等），并出 HTML 联系表。`fetch --sheet` 出本地联系表并检查真实宽高、完整解码；视频自动截首帧 poster。

贴图默认下载 1k Diffuse，`--maps all` 拉取 Diffuse、Roughness、OpenGL Normal JPG 并校验大小与 MD5；使用与许可见 [配图](media.md#真实贴图与科学工程素材)。下载及 poster 自动写入同目录 `SOURCES.md`，兼容 `fetch "<URL>" --out assets/<文件名> --note "来源说明"`。全部选项见 `node <skill>/scripts/curate-media.mjs --help`。

### 看结果

交给评审前先自己看一眼：默认状态是不是已经加载完，遮字版有没有把图形也一起盖掉。证据有错先重截，再交给评审。汇总里提示录屏或序列图和截图不一致时，静止的终态以截图为准，再单独查看那一段操作或补序列图核对过渡。序列图能判断状态与变化，不能据此宣称正常速度下的手感已验证。画面是空的 WebGL 截图不能当证据。

截图和取证优先用这里的截图工具。确实要自己写浏览器脚本（例如 Puppeteer 或 Playwright）时，启动参数加 `--use-mock-keychain --password-store=basic`，并用临时的用户数据目录；否则在 macOS 上会反复弹出钥匙串授权窗口，打断用户。

每张截图都会运行[三级质量门禁](quality-gates.md)的可观察规则，结果写进 `report.json` 的 `lint`；默认只提示，显式 `--gates` 才改变返回码。启发式提示清零之后仍要自己看截图。检查报出接口 401、404 这类和画面无关的错误时，在交付说明里记一行，不为了让检查通过去改登录、接口这类业务代码。

其中截图工具会检查：

- **文字对比度**：普通文字、输入框文字和占位文字低于 4.5:1，大字低于 3:1 时提示；真实底色含伪元素底板，图片、视频、canvas、背景图或渐变不明时跳过。
- **字号与行高**：可见文字或启用态文本控件小于 11px 时提示；多行正文含中文不少于 30 字、否则不少于 60 字符，行高中文低于 1.4 倍字号、英文低于 1.3 倍时提示。
- **入场与移动输入**：首屏内容停在透明状态时提示；手机视口内启用态文本控件小于 16px 时提示，避免聚焦触发 iOS 自动放大。
- **弹窗操作**：打开的表单弹窗里，提交按钮或最后一个按钮在视口外、或被内部滚动区域裁掉时提示；用 `--steps` 打开弹窗后才能检查。
- **横向溢出**：根宽超过视口 2px 且根节点未主动裁切时，报告最多 3 个可见越界元素和超出像素；裁切出血、局部轮播等不撑宽根文档的情况不报。

## 写可操作的小样

方向探索阶段的首屏不做交互，用不到这一节；选定方向后做完整页面时再用。存量项目优先沿用已安装的组件库、图标库、样式体系与技术栈。新建项目按用户约束、平台和主要交互选定组件基础；Joyally 自有 React Web（含 H5 与 Chrome 扩展）的主组件体系是 shadcn/ui。正式界面的控件来源先明确，已有工程或交付约定优先于下面的独立 HTML 小样做法。

独立小样不额外引入构建链，用原生脚本或轻量库实现真实的筛选、切换与详情交互。正式入口 HTML 的本地依赖放到同目录的 `vendor/` 再引用，过程小样及其依赖才放任务目录。
