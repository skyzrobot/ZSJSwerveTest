from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

SRC = r"C:\Users\Xiang\Desktop\Swerve\src\main\java\frc\robot"
OUT = r"C:\Users\Xiang\Desktop\Swerve代码逐行说明.docx"

CN_FONT = "微软雅黑"
CODE_FONT = "Consolas"


def set_font(run, name, size=None, bold=None, color=None):
    run.font.name = name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), CN_FONT)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = color


def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def mark_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def no_split(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def add_desc(cell, text, size=9):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.05
    parts = text.split("`")
    for i, part in enumerate(parts):
        if not part:
            continue
        run = p.add_run(part)
        if i % 2 == 1:
            set_font(run, CODE_FONT, size - 1, color=RGBColor(0x9C, 0x1F, 0x1F))
        else:
            set_font(run, CN_FONT, size)


def add_code(cell, code, size=8):
    lines = code.split("\n")
    first = True
    for ln in lines:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(ln if ln else " ")
        set_font(run, CODE_FONT, size)


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def line_table(doc, path, defs):
    lines = read_lines(path)
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [Cm(2.0), Cm(8.4), Cm(6.6)]
    hdr = table.rows[0]
    mark_header(hdr)
    for i, text in enumerate(["行", "代码", "作用"]):
        cell = hdr.cells[i]
        cell.width = widths[i]
        p = cell.paragraphs[0]
        run = p.add_run(text)
        set_font(run, CN_FONT, 9, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        shade(cell, "2F5597")
    for start, end, desc in defs:
        row = table.add_row()
        no_split(row)
        rng = f"{start}" if start == end else f"{start}–{end}"
        cell0 = row.cells[0]
        cell0.width = widths[0]
        run = cell0.paragraphs[0].add_run(rng)
        set_font(run, CN_FONT, 8.5, bold=True)
        cell1 = row.cells[1]
        cell1.width = widths[1]
        add_code(cell1, "\n".join(lines[start - 1:end]).strip("\n"))
        cell2 = row.cells[2]
        cell2.width = widths[2]
        add_desc(cell2, desc)
    doc.add_paragraph()


def two_col_table(doc, headers, rows, widths=(Cm(5.0), Cm(12.0))):
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    hdr = table.rows[0]
    mark_header(hdr)
    for i, text in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = widths[i]
        run = cell.paragraphs[0].add_run(text)
        set_font(run, CN_FONT, 9, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        shade(cell, "2F5597")
    for a, b in rows:
        row = table.add_row()
        no_split(row)
        row.cells[0].width = widths[0]
        row.cells[1].width = widths[1]
        run = row.cells[0].paragraphs[0].add_run(a)
        set_font(run, CN_FONT, 8.5, bold=True)
        add_desc(row.cells[1], b)
    doc.add_paragraph()


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    parts = text.split("`")
    for i, part in enumerate(parts):
        if not part:
            continue
        run = p.add_run(part)
        if i % 2 == 1:
            set_font(run, CODE_FONT, 9.5, color=RGBColor(0x9C, 0x1F, 0x1F))
        else:
            set_font(run, CN_FONT, 10)


def para(doc, text, size=10, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.2
    parts = text.split("`")
    for i, part in enumerate(parts):
        if not part:
            continue
        run = p.add_run(part)
        if i % 2 == 1:
            set_font(run, CODE_FONT, size - 0.5, color=RGBColor(0x9C, 0x1F, 0x1F))
        else:
            set_font(run, CN_FONT, size)


def code_block(doc, text, size=9):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(0.4)
    for i, ln in enumerate(text.split("\n")):
        if i:
            p.add_run().add_break()
        run = p.add_run(ln if ln else " ")
        set_font(run, CODE_FONT, size)


def heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        set_font(run, CN_FONT, 16 if level == 1 else 13, bold=True,
                 color=RGBColor(0x1F, 0x38, 0x64))
    return h


doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.left_margin = Cm(2.0)
sec.right_margin = Cm(2.0)
sec.top_margin = Cm(2.0)
sec.bottom_margin = Cm(2.0)

style = doc.styles["Normal"]
style.font.name = CN_FONT
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn("w:eastAsia"), CN_FONT)

footer_p = sec.footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer_p.add_run("FRC Swerve（Kraken X60 / X44 + MK5n）代码逐行说明")
set_font(fr, CN_FONT, 8, color=RGBColor(0x80, 0x80, 0x80))

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = title.add_run("FRC Swerve 代码逐行说明")
set_font(tr, CN_FONT, 26, bold=True, color=RGBColor(0x1F, 0x38, 0x64))

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sr = sub.add_run("Kraken X60 / X44 + SDS MK5n  ·  8 个电机 CAN ID 0–7  ·  lib/ironpulse 原版未改动")
set_font(sr, CN_FONT, 11, color=RGBColor(0x40, 0x40, 0x40))

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
mr = meta.add_run("工程：C:\\Users\\Xiang\\Desktop\\Swerve　|　目标：roboRIO 2026 + Phoenix 6 26.3.0")
set_font(mr, CN_FONT, 9, color=RGBColor(0x70, 0x70, 0x70))

doc.add_paragraph()

heading(doc, "一、这份文档说明什么", 1)
para(doc, "本文逐行解释机器人层（`frc.robot`）的 5 个主要文件（另加 `Main.java`），并给出整个工程的架构详解，以及机器人层里所有使用 lib 的地方的说明。")
para(doc, "行号对应当前工程中的实际行号；表格第三列是这一行（或这几行组成的一条语句）的作用。")
para(doc, "`lib/ironpulse` 是第三方库，共 94 个文件，保持原样、未做任何修改；它缺失的 `*ParamsNT` 生成类由 `src/ext` 里的注解处理器在构建时生成，不落在 lib 源码目录里。")

heading(doc, "二、文件架构详解", 1)
para(doc, "工程按“应用层 → 控制层 → 硬件层”三层组织，另外还有构建期自动生成的两类代码（NT 参数类与日志 inputs 类）。")

heading(doc, "2.1 目录结构", 2)
code_block(doc, """Swerve/
├─ src/main/java/
│  ├─ frc/robot/                    应用层（你维护的 6 个文件）
│  │  ├─ Main.java                  程序入口
│  │  ├─ Robot.java                 LoggedRobot 主类
│  │  ├─ RobotContainer.java        装配 + 摇杆驱动
│  │  ├─ Constants.java             全部常量
│  │  ├─ SwerveModuleParams.java    PID 默认值（@NTParameter 源）
│  │  └─ FieldConstants.java        场地长宽
│  └─ lib/ironpulse/                第三方库（94 个文件，原版未改）
│     ├─ swerve/                    Swerve、Module、Config、Setpoint、Limit
│     │  ├─ mk5n/                   Pigeon / TalonFX / CANcoder 实现
│     │  ├─ commands/               库自带命令（本项目未使用）
│     │  └─ sim/                    仿真 IO（本项目未使用）
│     ├─ limelight/ indicator/ ...  视觉、LED 等（保留但未使用）
│     └─ math/ utils/               数学与通用工具
├─ src/ext/java/lib/ntext/          NT 参数注解处理器（构建期运行）
├─ vendordeps/                      Phoenix6、AdvantageKit、PathPlanner、REV
└─ build/generated/                 构建时生成的 *ParamsNT 与 *AutoLogged""")

heading(doc, "2.2 三层结构与依赖方向", 2)
code_block(doc, """frc.robot（应用层）
   │  new + 传配置 / 传接口实现
   ▼
lib.ironpulse.swerve（控制层）
   Swerve → SwerveModule → SwerveModuleIO / ImuIO（接口）
   │  实现由 mk5n 提供
   ▼
lib.ironpulse.swerve.mk5n（硬件层）
   TalonFX × 2 + CANcoder + Pigeon2（真实 CAN 设备）""")
para(doc, "依赖只朝下：应用层 import lib，lib 不 new 应用层的类。lib 里只有两处反向引用：`SwerveModule` 用生成的 `frc.robot.SwerveModuleParamsNT` 读 PID，`AllianceFlipUtil` 用 `frc.robot.FieldConstants` 做红蓝翻转。")
para(doc, "`Swerve` 继承 `SubsystemBase`，所以 `new Swerve(...)` 之后会被 `CommandScheduler` 自动登记，`periodic()` 每 20 ms 自动执行，不需要手动调用。")

heading(doc, "2.3 构造顺序（顺序不能乱）", 2)
code_block(doc, """1) buildConfig()                         纯数据，不碰硬件
2) new SwerveModuleIOMK5N ×4             第一台创建静态 syncThread
3) SwerveModuleIOMK5N.startSyncThread()  启动 100 Hz 采样线程
4) new ImuIOPigeon(...)                  取同一个 syncThread
5) new Swerve(config, imu, ios)          建 Module / 运动学 / Setpoint / 估计器
6) setDefaultCommand(...)                绑定摇杆驱动""")
para(doc, "如果先建 Pigeon 再建模块，`ImuIOPigeon` 拿到的 `syncThread` 是 null，yaw 采样退化成单点，里程计只能跑到约 50 Hz。")

heading(doc, "2.4 运行期三条链", 2)
code_block(doc, """状态估计链
Robot.robotPeriodic → PhoenixUtils.refreshAll → CommandScheduler.run
 → Swerve.periodic
    → imuIO.updateInputs（yaw/pitch/roll + 高频队列）
    → 每个模块 updateInputs / periodic（位置样本 + PID 热更新）
    → getSampledModulePositions（时间戳对齐）
    → poseEstimator.updateWithTime

控制链
默认命令 drive()
 → ChassisSpeeds.fromFieldRelativeSpeeds(用 yaw 转场地坐标)
 → swerve.runTwist
    → setpointGenerator.generate（速度/加速度限幅）
    → module.runState
       → io.setDriveVelocity / io.setSteerAngleAbsolute
          → TalonFX.setControl(VelocityTorqueCurrentFOC / PositionDutyCycle)

独立采样链（不经过调度器）
PhoenixSynchronizationThread 每 10 ms 刷新信号并写入队列
 → updateInputs 把队列搬进 inputs.xxxSamples""")

heading(doc, "2.5 构建期生成链", 2)
para(doc, "`src/ext` 里的 `NTParameterProcessor` 在编译主源码时扫描 `@NTParameter` 类，并生成对应的 NT 门面类：")
code_block(doc, """@NTParameter 源                                生成到 build/generated
frc.robot.SwerveModuleParams             →     frc.robot.SwerveModuleParamsNT
lib...commands.SwerveDriveToPose 等 3 个 →     同名 ParamsNT
所有 @AutoLog 的 IO inputs               →     *AutoLogged""")
para(doc, "生成类属于编译产物，不写进 `src/main/java`，所以 lib 目录保持原版。")

heading(doc, "三、CAN ID 分配", 1)
two_col_table(doc, ["模块", "驱动电机 / 转向电机 / CANcoder"], [
    ("FrontLeft", "0 / 1 / 8"),
    ("FrontRight", "2 / 3 / 9"),
    ("BackLeft", "4 / 5 / 10"),
    ("BackRight", "6 / 7 / 11"),
    ("Pigeon 2.0", "20（roboRIO 总线）"),
])
para(doc, "八个电机的 ID 固定为 0–7；CANcoder 用 8–11，因为同一根总线上设备 ID 不能重复。要改只在 `Constants.java` 改一处。")

heading(doc, "四、Robot.java（26 行）", 1)
line_table(doc, os.path.join(SRC, "Robot.java"), [
    (1, 1, "包名 `frc.robot`。"),
    (3, 3, "导入命令调度器。"),
    (4, 4, "导入 `PhoenixUtils`：批量刷新 CTRE 状态信号。"),
    (5, 5, "导入 `NTParameterRegistry`：lib 的可调参数注册表（来自 `src/ext`）。"),
    (6, 6, "导入 AdvantageKit 的 `LoggedRobot`。"),
    (7, 7, "导入 `Logger`。"),
    (8, 8, "导入 NT4 日志发布器。"),
    (10, 10, "主类继承 `LoggedRobot`；AdvantageKit 强制要求如此。"),
    (11, 11, "保存 `RobotContainer` 引用。"),
    (13, 13, "构造函数。"),
    (14, 14, "`super(0.02)`：设定 20 ms 主循环周期。"),
    (15, 15, "注册 NT4 发布器，日志可被 AdvantageScope 实时查看。"),
    (16, 16, "启动 Logger；lib 里的 `Logger.processInputs/recordOutput` 依赖它。"),
    (17, 17, "创建容器：真正构造 8 台 TalonFX、4 个 CANcoder、Pigeon。"),
    (20, 20, "覆盖 `robotPeriodic`。"),
    (21, 21, "每 20 ms 执行一次。"),
    (22, 22, "`NTParameterRegistry.refresh()`：从 NT 读最新 PID 并推进“已变化”状态；不加会把 PID 配置每轮重下一次。"),
    (23, 23, "`PhoenixUtils.refreshAll()`：刷新所有已注册的 `StatusSignal`。"),
    (24, 24, "运行命令调度器：触发各子系统 `periodic()` 并执行命令。"),
    (25, 25, "方法结束。"),
    (26, 26, "类结束。"),
])

heading(doc, "五、RobotContainer.java（80 行）", 1)
line_table(doc, os.path.join(SRC, "RobotContainer.java"), [
    (1, 1, "包名。"),
    (3, 3, "静态导入单位。"),
    (5, 5, "导入 `ChassisSpeeds`（底盘速度）。"),
    (6, 6, "导入 `Commands`，用 `Commands.run(...)` 建默认命令。"),
    (7, 7, "导入 Xbox 手柄类。"),
    (8, 12, "导入 lib：`Swerve`、`SwerveConfig`、Pigeon IO、MK5N 配置与模块 IO。"),
    (14, 14, "类声明。"),
    (15, 15, "构建 MK5N 配置（只构建一次）。"),
    (16, 16, "`Swerve` 字段，在构造里赋值（因为要先建 IO）。"),
    (17, 17, "0 号 USB 口的 Xbox 手柄。"),
    (19, 19, "构造函数。"),
    (20, 20, "建 4 个模块 IO 的数组。"),
    (21, 21, "遍历 4 个模块。"),
    (22, 22, "`new SwerveModuleIOMK5N(config, i)`：创建该模块的 TalonFX×2 + CANcoder 并写配置。"),
    (23, 23, "循环结束。"),
    (24, 24, "启动 100 Hz Phoenix 采样线程（模块与 Pigeon 共用）。"),
    (25, 25, "构造 `Swerve`：传配置、Pigeon IO、4 个模块 IO。"),
    (26, 26, "把摇杆驱动设为默认命令，占用 `Swerve` 子系统。"),
    (27, 27, "构造结束。"),
    (29, 29, "`drive()`：每 20 ms 由默认命令调用。"),
    (30, 30, "从限幅取最大线速度（4.6 m/s）。"),
    (31, 31, "从限幅取最大角速度（9 rad/s）。"),
    (32, 32, "`x = -左摇杆Y × maxSpeed`：往前推为正。"),
    (33, 33, "`y = -左摇杆X × maxSpeed`：往左推为正（WPILib 的 y 向左）。"),
    (34, 34, "`omega = -右摇杆X × maxOmega`：右推为顺时针（负）。"),
    (35, 37, "用当前估计位姿的 yaw 把“场地坐标系”速度转成“机器人坐标系”，交给 `runTwist`。"),
    (40, 40, "`buildConfig()`：组装 `SwerveMK5NConfig`。"),
    (41, 42, "建 4 个 `SwerveModuleConfig` 的数组。"),
    (43, 43, "遍历 `Constants.kModules`。"),
    (44, 44, "取出当前模块常量。"),
    (45, 56, "用 builder 填：名字、位置、驱动/转向/CANcoder ID、CANcoder 偏置、驱动反向、转向反向、编码器不反向。"),
    (57, 57, "模块循环结束。"),
    (59, 78, "构建 `SwerveMK5NConfig`：日志名、周期、轮径、两个齿轮比、Kt、质量、Pigeon 配置、两套限幅、模块数组、4 个电流限制、里程计频率、CAN 总线、Pigeon ID。"),
    (79, 79, "方法结束。"),
    (80, 80, "类结束。"),
])

heading(doc, "六、Constants.java（132 行）", 1)
line_table(doc, os.path.join(SRC, "Constants.java"), [
    (1, 1, "包名。"),
    (3, 3, "静态导入单位，便于写 `MetersPerSecond.of(...)`。"),
    (5, 5, "导入 `CANBus`。"),
    (6, 6, "导入 `Translation2d`（模块位置）。"),
    (7, 11, "导入 `Angle`/`Current`/`Distance`/`Frequency`/`Mass` 单位类型。"),
    (12, 14, "导入 `ImuPigeonConfig`、`SwerveLimit`、`SwerveModuleLimit`。"),
    (16, 16, "`final` 常量类。"),
    (17, 17, "私有构造，禁止实例化。"),
    (19, 19, "日志前缀 `Swerve`。"),
    (21, 28, "八个电机 ID：FL 驱动 0/转向 1，FR 2/3，BL 4/5，BR 6/7。"),
    (30, 33, "四个 CANcoder ID：8/9/10/11。"),
    (35, 35, "Pigeon2 的 ID = 20。"),
    (36, 36, "CAN 总线 = roboRIO 板载 CAN。"),
    (38, 38, "控制周期 20 ms，Setpoint 生成器用它限加速度。"),
    (39, 39, "里程计采样 100 Hz。"),
    (41, 41, "轮径 4 英寸。"),
    (42, 42, "驱动减速比 6.03（MK5n R2）。"),
    (43, 43, "转向减速比 26.09（MK5n）。"),
    (44, 44, "Kraken X60 转矩常数 ≈0.0194 N·m/A，仅用于力矩估计日志。"),
    (45, 45, "整车质量 60 kg。"),
    (47, 47, "半轴距 0.30 m。"),
    (48, 48, "半轮距 0.30 m（合起来 0.6×0.6 m）。"),
    (50, 53, "四个电流限制：驱动定子 80 A / 供电 60 A，转向定子 40 A / 供电 30 A。"),
    (55, 55, "Pigeon 配置用库默认值（安装姿态 pitch=90，X 轴朝上）。"),
    (57, 64, "底盘限幅：4.6 m/s、加速 12 m/s²、刹车 14 m/s²、角速度 9 rad/s、角加速度 36 rad/s²。"),
    (66, 73, "模块限幅：轮速 5.0 m/s、加速 30、减速 35、转向 24 rad/s、转向角加速度 240 rad/s²。"),
    (75, 83, "`ModuleConfig` 记录：名字/位置/三个 ID/CANcoder 偏置/两个反向标志。"),
    (85, 94, "前左模块：位置 (+0.3, +0.3)，ID 0/1/8，偏置 0，不反向。"),
    (96, 105, "前右模块：位置 (+0.3, −0.3)，ID 2/3/9。"),
    (107, 116, "后左模块：位置 (−0.3, +0.3)，ID 4/5/10。"),
    (118, 127, "后右模块：位置 (−0.3, −0.3)，ID 6/7/11。"),
    (129, 131, "四模块数组，顺序必须和运动学一致。"),
])

heading(doc, "七、SwerveModuleParams.java（22 行）", 1)
para(doc, "这个类只提供 PID 默认值；运行时读的是构建时生成的 `SwerveModuleParamsNT`。")
line_table(doc, os.path.join(SRC, "SwerveModuleParams.java"), [
    (1, 1, "包名。"),
    (3, 3, "导入 `@NTParameter` 注解。"),
    (5, 5, "标注表名 `Params/SwerveModule`，编译期由 `NTParameterProcessor` 生成 `SwerveModuleParamsNT`。"),
    (6, 6, "类；只作为默认值来源，运行时用生成类。"),
    (7, 7, "驱动参数组。"),
    (8, 8, "驱动 kP = 6.0（转矩电流环，单位 A/(电机 rps)）。"),
    (9, 9, "驱动 kI = 0。"),
    (10, 10, "驱动 kD = 0。"),
    (11, 11, "驱动 kS = 0。"),
    (12, 12, "驱动 kV = 0.136。"),
    (13, 13, "驱动 kA = 0.05。"),
    (16, 16, "转向参数组。"),
    (17, 17, "转向 kP = 60.0（位置环，输出为占空比）。"),
    (18, 18, "转向 kI = 0。"),
    (19, 19, "转向 kD = 0.1。"),
    (20, 20, "转向 kS = 0。"),
    (22, 22, "类结束。"),
])

heading(doc, "八、FieldConstants.java 与 Main.java", 1)
line_table(doc, os.path.join(SRC, "FieldConstants.java"), [
    (1, 1, "包名。"),
    (3, 3, "`final` 类。"),
    (4, 4, "私有构造。"),
    (6, 6, "场地长 16.541 m。"),
    (7, 7, "场地宽 8.069 m；`AllianceFlipUtil` 用它做红蓝翻转。"),
    (8, 8, "类结束。"),
])
para(doc, "`Main.java` 是模板文件，未改动：第 14 行私有构造，第 22–24 行 `main` 里调用 `RobotBase.startRobot(Robot::new)`。")

heading(doc, "九、所有使用 lib 的内容", 1)
para(doc, "这一节按“用到了哪个 lib 类 / 接口、在哪里用、lib 内部拿它做什么”说明，覆盖机器人层对 lib 的全部引用。")

heading(doc, "9.1 引用清单", 2)
two_col_table(doc, ["lib 类型", "使用位置与作用"], [
    ("`Swerve`", "RobotContainer:16/25/26/35。子系统本体：构造时建模块、运动学、Setpoint 生成器、位姿估计器；`setDefaultCommand` 绑定驱动；`runTwist` 下发速度；`getEstimatedPose` 供场地坐标转换。"),
    ("`SwerveMK5NConfig`", "RobotContainer:15/59–78。MK5N 专用配置：在 `SwerveConfig` 基础上增加 CAN 总线、Pigeon ID、里程计频率、四个电流限制。"),
    ("`SwerveConfig` 及内部 `SwerveModuleConfig`", "RobotContainer:41–56。底盘级配置：周期、轮径、齿轮比、Kt、质量、限幅、模块数组；每个模块的位置/三个 ID/偏置/反向。"),
    ("`SwerveModuleIOMK5N`", "RobotContainer:22、24。实现 `SwerveModuleIO`：TalonFX 驱动/转向 + CANcoder 的实际读写；`startSyncThread()` 启动采样线程。"),
    ("`ImuIOPigeon`", "RobotContainer:25。实现 `ImuIO`：Pigeon2 的配置与 yaw/pitch/roll 读取。"),
    ("`SwerveLimit`", "Constants:57–64。底盘速度/加速度上限，交给 `SwerveSetpointGenerator` 使用。"),
    ("`SwerveModuleLimit`", "Constants:66–73。模块轮速/转向速度上限。"),
    ("`ImuPigeonConfig`", "Constants:55。Pigeon 安装姿态、陀螺 trim、罗盘开关。"),
    ("`frc.robot.SwerveModuleParamsNT`（生成）", "lib 的 `SwerveModule:37–54、85–86` 读取驱动/转向增益，并在参数变化时下发电机配置。"),
    ("`NTParameterRegistry`（src/ext）", "Robot:22。每轮刷新 NT 参数并推进“已变化”状态。"),
    ("`PhoenixUtils`", "Robot:23。`refreshAll()` 刷新所有注册过的 CTRE `StatusSignal`。"),
    ("`Localizable`（limelight）", "由 `Swerve` 实现（`addVisionMeasurement`/`getIMUYaw`/`setIMUYaw`），是以后接视觉的接口，本项目暂未使用。"),
    ("`Logger`（AdvantageKit）", "Robot:15–16 启动；lib 内部用它记录模块/IMU/位姿。"),
    ("`SwerveCommands` 等库命令", "未使用。驾驶逻辑写在 `RobotContainer.drive()`；需要时可直接改用 `SwerveCommands.driveWithJoystick`。"),
])

heading(doc, "9.2 配置字段被 lib 的哪个部分消费", 2)
two_col_table(doc, ["配置字段", "lib 内部消费点"], [
    ("`name`", "日志前缀：`Swerve/IMU`、`Swerve/Module/<name>`"),
    ("`dtS`", "`SwerveSetpointGenerator.generate(...)` 的积分步长，决定加减速限幅幅度"),
    ("`wheelDiameter`", "轮速 ↔ 线速度、轮位置 ↔ 电机位置换算（`SwerveModule`、`SwerveModuleIOMK5N`）"),
    ("`driveGearRatio`", "电机转速 ↔ 轮速、电机位置 ↔ 轮位置（`SwerveModuleIOMK5N` 的换算函数）"),
    ("`steerGearRatio`", "`FusedCANcoder` 的 `RotorToSensorRatio`（26.09:1）"),
    ("`driveMotorKt`", "`Swerve.getWrench()` 用转矩电流估算轮上力（日志）"),
    ("`driveMass`", "供整车动力学/日志使用（该字段在库中预留）"),
    ("`steerMotorEncoderOffset`", "CANcoder 的 `MagnetOffset`，把绝对零点对齐到轮子正前方"),
    ("`driveInverted`", "驱动电机 `MotorOutput.Inverted`"),
    ("`steerInverted`", "转向电机 `MotorOutput.Inverted`"),
    ("`encoderInverted`", "CANcoder 的 `SensorDirection`"),
    ("`defaultSwerveLimit`", "`SwerveSetpointGenerator` 的底盘限幅"),
    ("`defaultSwerveModuleLimit`", "模块级限幅（轮速、转向速度）"),
    ("`moduleConfigs[i].location`", "运动学安装位置 + X 锁角度预计算"),
    ("`moduleConfigs[i].drive/steer/encoderId`", "`new TalonFX/CANcoder` 的设备 ID"),
    ("`driveStator/SupplyCurrentLimit`", "驱动电机 `CurrentLimits` 配置"),
    ("`steerStator/SupplyCurrentLimit`", "转向电机 `CurrentLimits` 配置"),
    ("`odometryFrequency`", "采样线程频率 + 位置信号 `setUpdateFrequency`"),
    ("`canivoreCanBus`", "所有 TalonFX / CANcoder / Pigeon 构造时使用的总线"),
    ("`pigeonId`", "`new Pigeon2(id, bus)`"),
    ("`pigeonConfig`", "Pigeon2 的安装姿态、陀螺 trim、罗盘开关"),
])

heading(doc, "9.3 机器人层的调用如何落到硬件", 2)
two_col_table(doc, ["你的代码", "lib 内部发生的动作"], [
    ("`new SwerveModuleIOMK5N(config, i)`", "创建 TalonFX×2 + CANcoder → 写反向/电流/反馈配置 → 注册 StatusSignal 与采样队列"),
    ("`new ImuIOPigeon(...)`", "创建 Pigeon2 → 写安装姿态/trim → 注册 yaw 采样队列"),
    ("`new Swerve(...)`", "建 4 个 `SwerveModule` → 运动学 → Setpoint 生成器 → 3D 位姿估计器"),
    ("`swerve.setDefaultCommand(...)`", "`CommandScheduler` 每轮调用 `drive()`"),
    ("`swerve.getEstimatedPose()`", "位姿估计器输出（轮式里程计 + Pigeon yaw）"),
    ("`swerve.runTwist(speeds)`", "限幅 → 运动学分解 → `module.runState` → TalonFX 速度环/位置环"),
    ("`PhoenixUtils.refreshAll()`", "刷新所有注册的 `StatusSignal`，供 `updateInputs` 读取"),
    ("`NTParameterRegistry.refresh()`", "读 NT → 更新 wrapper → `SwerveModule` 发现变化后重下 PID"),
])

heading(doc, "9.4 lib 反向依赖你提供的符号", 2)
para(doc, "lib 不 new 你的类，但有两处直接引用（这是它能编译的前提）：")
two_col_table(doc, ["lib 文件", "需要的符号 / 你提供的位置"], [
    ("`SwerveModule.java:10`", "`frc.robot.SwerveModuleParamsNT` —— 由 `frc.robot.SwerveModuleParams` 在构建期生成，源码里没有这个文件"),
    ("`AllianceFlipUtil.java:12`", "`frc.robot.FieldConstants` —— 你项目里的 `FieldConstants.java` 提供 `fieldLength` / `fieldWidth`"),
])

heading(doc, "9.5 未使用但保留的 lib 能力", 2)
bullet(doc, "`SwerveCommands.driveWithJoystick`：带死区、曲线、场地坐标的现成驱动命令，可替换 `RobotContainer.drive()`。")
bullet(doc, "`SwerveCommands.driveToPose` / `followPathPlannerTrajectory` / `xLock` / `sysid`：自动对准、路径跟随、X 锁、系统辨识。")
bullet(doc, "`LimelightSubsystem`：视觉定位；`Swerve` 已实现 `Localizable`，可以直接把 `swerve` 传进去。")
bullet(doc, "`IndicatorSubsystem`、`BeamBreak`、`MotorSubsystem`：LED、光电、通用电机子系统。")
bullet(doc, "`SwerveModuleIOSim` / `ImuIOSim`：不接硬件跑仿真，构造 `Swerve` 时替换 IO 即可。")

heading(doc, "十、运行要点与标定", 1)
para(doc, "1. `NTParameterRegistry.refresh()` 不能删（Robot.java 第 22 行）。")
para(doc, "它负责把 NT 值和 `prevValue` 同步。少了它，`NTParameterWrapper.hasChanged()` 永远为 true，`SwerveModule.periodic()` 每 20 ms 重下一次 PID 配置，日志会出现 `Do not apply or refresh configs periodically`，循环时间会涨到 0.25 s 左右。")
para(doc, "2. Pigeon 安装姿态（Constants.java 第 55 行）。")
para(doc, "库默认 `mountPosePitch=90`，即 Pigeon 的 X 轴朝上安装。如果把 Pigeon 平放（Z 轴朝上，最常见），要改成：")
code_block(doc, "ImuPigeonConfig.builder().mountPosePitch(0).build()")
para(doc, "否则 yaw 会整体错 90°，车会“斜着走”。同时 Pigeon 的 X 轴要指向车头。")
para(doc, "3. CANcoder 零位（Constants.java 第 85–127 行的偏置）。")
para(doc, "现在四个偏置都是 `Rotations.of(0.0)`，实车必须标定：把轮子摆正朝前，读该 CANcoder 的绝对位置 p，把偏置改成 `Rotations.of(-p)`。")
para(doc, "4. 电流限制为什么还在。")
para(doc, "`SwerveMK5NConfig` 与 `SwerveModuleIOMK5N` 依赖这 4 个字段，要彻底删掉必须改 lib；按“不要改 lib”的要求，把它们保留为 `Constants` 里的配置值（80/60/40/30 A），需要时只改常量即可。")
para(doc, "5. 方向反了怎么办。")
para(doc, "转向“越转越飞”把该模块 `steerInverted` 改 true；驱动方向反了改 `driveInverted`。不要反复拆电机三相线。")

heading(doc, "十一、常见修改点对照", 1)
two_col_table(doc, ["想改什么", "改哪里"], [
    ("CAN ID", "`Constants.java` 第 21–33 行"),
    ("轮径 / 齿轮比 / Kt / 质量", "`Constants.java` 第 41–45 行"),
    ("电流限制", "`Constants.java` 第 50–53 行"),
    ("限速度 / 限角速度 / 限加速度", "`Constants.java` 第 57–73 行"),
    ("模块位置 / 是否反向 / CANcoder 偏置", "`Constants.java` 第 85–127 行"),
    ("Pigeon 安装方向", "`Constants.java` 第 55 行"),
    ("换 CANivore", "`Constants.java` 第 36 行改成 `new CANBus(\"canivore\")`"),
    ("PID 增益", "`SwerveModuleParams.java` 第 8–20 行（编译期默认值），运行时可在 NT 表 `Params/SwerveModule` 调"),
    ("摇杆手感 / 速度缩放", "`RobotContainer.java` 第 30–34 行"),
])

heading(doc, "十二、验证记录", 1)
bullet(doc, "`gradlew clean build`：BUILD SUCCESSFUL。")
bullet(doc, "直接运行生成的 fat jar：输出 `Robot program startup complete`，`Swerve.periodic()` 正常循环。")
bullet(doc, "仿真中只有“未接真实电机/CAN 数据过期”和“手柄未插”的预期警告，没有代码异常。")
bullet(doc, "lib 目录：94 个 .java 文件与 `Documents\\GitHub\\2026-offseason-robot-10541` 的 lib 逐字节一致。")
bullet(doc, "缺失的 `*ParamsNT` 由 `src/ext` 的注解处理器在构建时生成，位于 `build/generated/sources/annotationProcessor/...`。")

doc.core_properties.title = "FRC Swerve 代码逐行说明"
doc.core_properties.subject = "Kraken X60/X44 + MK5n"
doc.core_properties.author = "Swerve 项目"

doc.save(OUT)
print("saved", OUT, os.path.getsize(OUT))
