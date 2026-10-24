# 新政策规则明细(2026-11-03 生效)

核对日期:2026-10-24,逐条对过 IRCC 官方页面。**官方原文**与**官方没写**分开标;
回答用户时保持这个区分,不要把推断说成官方结论。

## 来源(出结论前优先重读这几个,政策页会改)

| 页面 | 用途 |
|---|---|
| https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/changes.html | **劳动力市场融合因子(LMIF)怎么算**:工作经验与 offer 二选一、最高 150 的构成 |
| https://www.canada.ca/en/immigration-refugees-citizenship/news/2026/10/changes-to-express-entry-for-high-wage-occupations.html | 政策公告:加分数值、offer 要求(页面日期 2026-10-16) |
| https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score/high-wage.html | 186 个 NOC 的档位表(已存 `high-wage-noc-list.tsv`) |
| https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score/crs-criteria.html | CRS 基础分表(`crs_calc.py` 里的表即来自此页) |
| https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/documents/job-offer.html | offer 文件要求 |

## 劳动力市场融合因子 = 两条路线取高(官方原文)

> "You can only receive points for Canadian work experience or an eligible job offer, **not both**."
> "You'll get the score that gives you the higher number of CRS points."
> "You can get a maximum of 150 points for the Labour Market Integration factor."(单身;带配偶 140)

| | 构成 | 单身最高 |
|---|---|---|
| **工作经验路线** | 年限分(1年40、2年53、3年64、4年72、5年及以上80)**+** 高薪职业经验加分(满 12 个月:Tier 1 +70 / Tier 2 +40 / Tier 3 +20) | 80 + 70 = **150** |
| **OFFER 路线** | 固定分:Tier 1 100 / Tier 2 70 / Tier 3 50(非高薪职业 0) | 100 |

**LMIF = max(工作经验路线, OFFER 路线)。** OFFER 分**不会**加在年限分上面;150 是工作经验路线自然的最大值(80+70),不是"加完再封顶"。

- 档位由**职业**的全国工资中位数(2023–2025 数据)决定:Tier 1 ≥ 2×、Tier 2 ≥ 1.5×、Tier 3 ≥ 1.3× 全职业平均中位数。
  **不是候选人自己的工资,也不是省级工资。** 工资只影响 offer 的合理性。
- 经验加分一般须在过去 10 年内、TEER 0–3 职业,且是**该高薪职业**的满 12 个月经验。
- Offer:一般须全职、PR 后**连续至少 1 年**;不再需要 LMIA;officer 必须认定 offer **真实**(雇主在实际经营、
  岗位需求合理、雇主有能力履行条款);被撤销的 offer 不算。
- 2026-11-03 当天及以后获邀的人,FSW/FST 项目下也免 LMIA 相关要求(临时公共政策,需满足其条件)。
- 公告建议可能受益者在 **11-03 之前**检查并更新档案;CRS 标准页称系统会在生效时对现有档案重新计算。
- 官方强调:"加分不保证获邀",要看每轮分数线。

### 由此推出的几个实际结论(都已用计算器验证,见 `test_crs_calc.py`)

- **有 12 个月以上、在清单职业上的加拿大经验的人,经验路线一定 ≥ offer 路线**(40+70=110 > 100,40+40=80 > 70,
  40+20=60 > 50)。所以对 CEC 候选人,新政策的实际增量是**经验加分**(+70/+40/+20),offer 分不会再多给。
- **OFFER 路线只在 offer 分高于你的"年限分 + 经验加分"时才有用**:例如经验不在清单职业上、或几乎没有加拿大经验。
  满 1 年、经验不在清单上、拿 Tier 2 offer:max(40, 70) = 70,只比原来多 30。
- 5 年经验 + Tier 1 **经验**:80 → 150(+70);5 年经验 + Tier 1 **offer 但经验不在清单**:80 → 100(只 +20)。
- 单身理论上限 676 = 年龄 110 + 硕士 135 + 语言 136 + LMIF 150 + 转换性 100 + 加拿大教育 30 + 兄弟姐妹 15
  (不含法语/博士);没有新政策是 606。**要拿满必须有 Tier 1 经验,单靠 Tier 1 offer 只有 100。**
- 表姐/堂姐不算兄弟姐妹,不加 15。

## 官方没写(别替它补)

- offer 是否必须书面。
- 池内现有档案重算的具体细节(CRS 标准页只说"系统会重新计算");第三方称重算期间抽签最多暂停两周,未见官方原文。
  系统里 offer 相关字段(含 LMIA 占位)**必须由中介或 IRCC 确认,不要自己填**。
- 同分排序规则:公告未写。"按档案提交时间,先提交者优先;编辑不重置、删除重建才重置"来自二手来源,只能说"据报道"。
- 技工与医生的特殊 offer 要求。
- 页面里有一处看起来矛盾:一张表给了统一的"100 分 offer",而公告与分档列表是 100/70/50。本 skill 以分档为准,
  11 月 3 日后用官方计算器核对。
- 新政后各类抽签的分数线走势(只能观察,见 `market-snapshot-2026-10.md`)。

## 这个 skill 自己犯过的错(留作教训)

第一版把公式写成 `min(150, 年限分 + max(经验加分, offer 加分))`——即 OFFER **加在**年限分上面、再封顶 150。
这是错的:它和官方"二选一取高"矛盾,对有加拿大经验的人**最多高估 70 分**。
发现过程:拿一个独立的开源实现(8,424 个生成档案)对拍,不含新政策的部分 0 个差异,含新政策的部分 4,698 个差异,
且全部是我们高估;再用官方 `changes.html` 原文裁决。**教训:官方说"最高 150"时,先找 150 的构成,别用"封顶"去凑数字。**

## 真实性与合规(给用户算分时一并提醒)

- 取消 LMIA 后,假 offer、小公司乱开 offer 的风险上升,officer 会查真实性;**虚假陈述 = 5 年禁入**。
  用户的工资单、T4、纳税记录都是强证据,让用户保持材料与事实一致。
- 同一份工作不能在不同材料里换说法重复报(例如公司项目和个人兼职);职称、职责、起止日期各份文件必须自洽。
  雇主信与 offer 里的职称/职责/时间不一致时,先让 HR 出变更说明,不要两份矛盾的文件一起交。
- 雇主信写法:就事实改,不替用户编造职责;未核实的职责先让用户确认。
- 合同类型(contract / permanent)不是加分条件本身,关键是 offer 满足"全职、PR 后至少连续一年"且被认定为真实;
  措辞要和雇佣合同事实一致,不要为了好看写成合同里没有的承诺。

## 常见算错的地方

- 把"经验加分 + offer 加分"相加(40+70)——不能叠加。
- **把 offer 分加在年限分上面**(上面那个错)——offer 路线是独立的固定分,和年限分二选一。
- 把"最高 170"(70+100)当真:不成立,最高 150。
- 把 12 个月经验的 NOC 默认等同于 offer 的 NOC:只有当那份工作真的在清单上才有经验加分,要分别问清。
- 手心算容易错,一律用 `scripts/crs_calc.py` 算,算完再解释。
