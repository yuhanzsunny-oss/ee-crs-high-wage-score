# 新政策规则明细(2026-11-03 生效)

核对日期:2026-10-23,逐条对过 IRCC 三个官方页面。**官方原文**、**推断**、**官方没写**三类分开标,
回答用户时保持这个区分,不要把推断说成官方结论。

## 来源(出结论前优先重读这几个,政策页会改)

| 页面 | 用途 |
|---|---|
| https://www.canada.ca/en/immigration-refugees-citizenship/news/2026/10/changes-to-express-entry-for-high-wage-occupations.html | 政策公告:加分数值、offer 要求(页面日期 2026-10-16) |
| https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score/high-wage.html | 186 个 NOC 的档位表(已存 `high-wage-noc-list.tsv`) |
| https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score/crs-criteria.html | CRS 基础分表(`crs_calc.py` 里的表即来自此页) |
| https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/documents/job-offer.html | offer 文件要求 |

## 官方原文确认的

**两条加分路线,取高不叠加**(原文:"whichever option provides more points";"will not be combined")

| 档位 | 判定(职业全国工资中位数 ÷ 全职业平均中位数) | 12 个月加拿大工作经验路线 | 合格 offer 路线 |
|---|---|---|---|
| Tier 1 | ≥ 2× | +70 | +100 |
| Tier 2 | ≥ 1.5× 且 < 2× | +40 | +70 |
| Tier 3 | ≥ 1.3× 且 < 1.5× | +20 | +50 |

- 档位看的是**这个职业**的全国中位数(2023–2025 数据),**不是候选人自己的工资,也不是省级工资**。
  工资只影响 offer 的合理性,不决定档位。
- 加分是在原有"按年限给的加拿大工作经验分"(1 年 40、2 年 53、3 年 64、4 年 72、5 年及以上 80)之上**再加**。
- 官方说加拿大工作经验分"可高达 150",且劳动力市场融合因子单身最高 150、带伴侣 140。
- 经验路线:一般须在过去 10 年内、TEER 0–3 职业。
- Offer:一般须是**全职(公告未写具体小时;IRCC 以往口径 ≥30 小时/周)**、在成为 PR 后**连续至少 1 年**;不再需要 LMIA;
  officer 必须认定 offer **真实**(雇主在实际经营、岗位需求合理、雇主有能力履行条款);被撤销的 offer 不算。
- 2026-11-03 当天及以后获邀的人,在 FSW/FST 项目下也免 LMIA 相关要求(临时公共政策,需满足其条件)。
- 公告建议:可能受益者应在 **11-03 之前**检查并更新 Express Entry 档案,确认 offer 信息完整准确。
- 官方强调:"加分不保证获邀",要看每轮的分数线。

## 推断(不是官方原文,务必标注)

- **150 上限如何合成**:官方没有解释。脚本采用
  `加拿大工作项 = min(150, 年限分 + max(经验加分, offer 加分))`。
  这个公式与官方"最高 150"的描述一致,并给出 676 的理论上限(5 年经验 + Tier 1 offer 只多 +70),
  但仍是反推。**11-03 之后要对着官方 CRS 页和 Express Entry 的"check your score"工具重新核对。**
- 5 年经验 + Tier 1 offer 只多得 70(80+100=180 → 封顶 150),而 1 年经验 + Tier 1 offer 可多得 100。
  这是上面公式的结果,不是官方举例。

## 官方没写(别替它补)

- offer 是否必须书面。
- 池内现有档案是否自动重算(CRS 标准页只说"系统会在 11-03 起对现有档案重新计算",未给细节)。
  实务上仍应让中介在 11-03 前把 offer 信息录入;系统里的 offer 占位(LMIA 字段如何填)
  **必须由中介或 IRCC 确认,不要自己填**。
- 同分排序规则:公告未写。网上常见的"按档案提交时间,先提交者优先;编辑不重置、删除重建才重置"
  来自二手来源(CIC News),只能说"据报道",不可当官方规则。
- 技工与医生的特殊 offer 要求。
- 新政后各类抽签的分数线走势(只能观察,见 `market-snapshot-2026-10.md`)。

## 真实性与合规(给用户算分时一并提醒)

- 取消 LMIA 后,假 offer、小公司乱开 offer 的风险上升,officer 会查真实性;**虚假陈述 = 5 年禁入**。
  用户的工资单、T4、纳税记录都是强证据,让用户保持材料与事实一致。
- 同一份工作不能在不同材料里换说法重复报(例如公司项目和个人兼职);职称、职责、起止日期各份文件必须自洽。
  雇主信与 offer 里的职称/职责/时间不一致时,先让 HR 出变更说明,不要两份矛盾的文件一起交。
- 雇主信写法:就事实改,不替用户编造职责;未核实的职责先让用户确认。
- 合同类型(contract / permanent)不是加分条件本身,关键是 offer 满足"全职、PR 后至少连续一年、无限期或足够长"
  且被认定为真实;措辞要和雇佣合同事实一致,不要为了好看写成合同里没有的承诺。

## 常见算错的地方

- 把"经验加分 + offer 加分"相加(如 40+70):**不能叠加**,取高。
- 忘记 150 封顶:`5 年 + Tier 1 offer` 看起来 +100,实际只 +70。
- 把"最高 170"(70+100)当真:不成立。
- 理论最高分:676 = 年龄 110 + 硕士 135 + 语言 136 + 加拿大工作项 150 + 转换性 100 + 加拿大教育 30 + 兄弟姐妹 15
  (单身、不含法语/博士)。同一个人没有新政策是 606。**表姐/堂姐不算兄弟姐妹,不加 15。**
- 手心算容易错,一律用 `scripts/crs_calc.py` 算,算完再解释。
