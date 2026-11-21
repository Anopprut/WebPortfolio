"""Thai guides about n8n + LINE. Facts checked 2026-10-10 against official docs/pages (links in each guide).
Anything not tested against a live LINE channel says so in the text. No invented numbers."""

CHECKED = "2026-10-10"

ARTICLES = [
    dict(
        slug="line-notify-ended-n8n-alternative",
        title="LINE Notify เลิกให้บริการแล้ว ใช้อะไรแทนใน n8n",
        desc="LINE Notify ปิดบริการ 31 มี.ค. 2025 วิธีส่งข้อความเข้า LINE จาก n8n ต่อด้วย Messaging API: ตั้งค่า token ส่งผ่าน HTTP Request หรือโหนดชุมชน พร้อมข้อควรระวัง",
        faq=[
            ("LINE Notify ยังใช้ได้ไหม?", "ไม่ได้ LINE ประกาศปิดบริการ และตั้งแต่ 1 เมษายน 2025 ฟีเจอร์และ API ของ LINE Notify ใช้งานไม่ได้ทั้งหมด LINE แนะนำให้ย้ายไปใช้ Messaging API"),
            ("ใช้ Messaging API ส่งเข้ากลุ่มได้ไหม?", "ได้เมื่อเชิญบัญชี LINE Official Account (บอต) เข้ากลุ่มแล้วใช้ groupId เป็นผู้รับ แต่ต้องตรวจเงื่อนไขและโควตาข้อความของแพ็กเกจที่ใช้อยู่ในเอกสาร LINE"),
            ("ต้องมีบัญชี LINE Official Account ไหม?", "ต้องสร้าง Messaging API channel ใน LINE Developers Console ซึ่งผูกกับ LINE Official Account และผู้รับต้องเพิ่มบัญชีนั้นเป็นเพื่อนก่อนจึงจะส่งข้อความหากันได้"),
        ],
        body="""
<p><b>คำตอบสั้น:</b> LINE Notify หยุดให้บริการแล้ว (ประกาศ 7 ต.ค. 2024 ปิดจริง 31 มี.ค. 2025) ถ้า workflow n8n ของคุณเคยส่งแจ้งเตือนผ่านโหนด LINE ที่ใช้ Notify มันจะไม่ทำงานอีก ทางแทนที่ LINE แนะนำคือ <b>Messaging API</b> ซึ่งใช้ได้ผ่านโหนด HTTP Request ของ n8n โดยไม่ต้องติดตั้งอะไรเพิ่ม</p>
<p class="note">ตรวจข้อมูลเมื่อ {CHECKED} จาก <a href="https://developers.line.biz/en/news/tags/end-of-life">ประกาศ End of life ของ LINE Developers</a> และกระทู้ <a href="https://community.n8n.io/t/feature-request-new-node-for-line-integration-replacing-deprecated-line-notify/99302">ขอโหนด LINE ใหม่แทน Notify ในชุมชน n8n</a></p>

<h2>ขั้นตอนย้ายแบบเร็วที่สุด (ผ่าน HTTP Request)</h2>
<ol>
<li><b>สร้าง Messaging API channel:</b> เข้า LINE Developers Console → สร้าง Provider → สร้าง Messaging API channel (ผูกกับ LINE Official Account)</li>
<li><b>เก็บ 2 ค่า:</b> Channel access token (ใช้ส่งข้อความ) และ Channel secret (ใช้ตรวจลายเซ็น webhook) เก็บใน Credentials ของ n8n อย่าใส่ในตัว workflow</li>
<li><b>หาผู้รับ:</b> ต้องมี <code>userId</code> ของคนที่เพิ่มบอตเป็นเพื่อนแล้ว (ได้จาก webhook event) หรือ <code>groupId</code> ของกลุ่มที่เชิญบอตเข้า</li>
<li><b>เพิ่มโหนด HTTP Request</b> ตั้งค่าตามด้านล่าง</li>
</ol>
<pre><code>POST https://api.line.me/v2/bot/message/push
Authorization: Bearer {Channel access token}
Content-Type: application/json

{
  "to": "U1234567890abcdef...",
  "messages": [
    { "type": "text", "text": "ออเดอร์ใหม่เข้าแล้ว" }
  ]
}</code></pre>
<p>ข้อความหนึ่งคำขอใส่ได้ไม่เกิน 5 ข้อความ (<a href="https://github.com/line/line-openapi">ข้อกำหนด OpenAPI ทางการของ LINE</a>)</p>

<h2>หรือใช้โหนดชุมชน</h2>
<p>มีโหนดชุมชนบน npm ที่ครอบ Messaging API อยู่แล้ว เช่น <a href="https://github.com/elct9620/n8n-nodes-line-messaging">n8n-nodes-line-messaging</a> (MIT) มีส่ง ตอบ multicast ดึงโปรไฟล์ และตัวรับ webhook ที่ตรวจลายเซ็นให้ ผมตรวจเมื่อ {CHECKED} พบว่ามีโหลดราว 1,100 ครั้งต่อเดือน เวอร์ชันล่าสุดบน npm เผยแพร่เมื่อเดือนตุลาคม 2025 และตัวโปรเจกต์บน GitHub ยังมีการอัปเดตล่าสุดเมื่อเดือนกันยายน 2026 แต่เป็นโหนดของบุคคลที่สาม ควรอ่านโค้ดและตรวจการดูแลก่อนใช้ในงานจริง</p>

<h2>ข้อควรระวัง</h2>
<ul>
<li>การส่งข้อความหาผู้ใช้ไม่ได้ฟรีไม่จำกัด ให้ตรวจโควตาข้อความของแพ็กเกจ LINE Official Account ที่ใช้อยู่</li>
<li>Notify เดิมส่งเข้า "ตัวเรา" ได้ง่าย แต่ Messaging API ต้องให้ผู้รับเพิ่มบอตเป็นเพื่อนก่อน จึงเปลี่ยนวิธีคิดเล็กน้อย</li>
<li>บทความนี้อธิบายจากเอกสารทางการ ผมไม่ได้ทดสอบส่งข้อความจริงกับ channel ของผู้อ่าน</li>
</ul>
{AFFILIATE}
""",
    ),
    dict(
        slug="line-messaging-reply-push-multicast-broadcast",
        title="Reply, Push, Multicast, Broadcast ของ LINE ต่างกันอย่างไร",
        desc="เปรียบเทียบ 4 วิธีส่งข้อความของ LINE Messaging API พร้อมขีดจำกัดที่เอกสารทางการระบุ (5 ข้อความต่อคำขอ, multicast สูงสุด 500 คน) และวิธีเลือกใช้ใน n8n",
        faq=[
            ("Reply กับ Push ต่างกันอย่างไร?", "Reply ตอบกลับเหตุการณ์ที่เพิ่งเกิดขึ้นโดยใช้ reply token ที่ได้จาก webhook ส่วน Push ส่งหาผู้ใช้เมื่อไรก็ได้ด้วย userId แต่ Push ใช้โควตาข้อความของบัญชี"),
            ("Multicast ส่งได้กี่คน?", "ตามข้อกำหนด OpenAPI ของ LINE ระบุผู้รับได้สูงสุด 500 userId ต่อคำขอ และแต่ละคำขอใส่ข้อความได้ไม่เกิน 5 ข้อความ"),
            ("Broadcast ส่งหาใคร?", "ส่งหาผู้ใช้ทั้งหมดที่เพิ่มบัญชีเป็นเพื่อน ใช้ระวังเพราะกระทบผู้ใช้ทุกคน และตรวจโควตาก่อน"),
        ],
        body="""
<p><b>คำตอบสั้น:</b> ใช้ <b>Reply</b> เมื่อตอบสิ่งที่ผู้ใช้เพิ่งส่งมา, <b>Push</b> เมื่อต้องการส่งหาคนใดคนหนึ่งเอง, <b>Multicast</b> เมื่อส่งหาคนหลายคนที่ระบุชื่อไว้, <b>Broadcast</b> เมื่อส่งหาทุกคนที่เป็นเพื่อนกับบัญชี</p>
<p class="note">ตรวจข้อมูลเมื่อ {CHECKED} จาก <a href="https://github.com/line/line-openapi">ข้อกำหนด OpenAPI ทางการของ LINE</a> ค่าโควตาและราคาข้อความเปลี่ยนตามแพ็กเกจ ให้ดูที่เอกสาร LINE ล่าสุด</p>

<table><tr><th>วิธี</th><th>ปลายทาง (endpoint)</th><th>ส่งหาใคร</th><th>ขีดจำกัดตามเอกสาร</th></tr>
<tr><td>Reply</td><td><code>POST /v2/bot/message/reply</code></td><td>คนที่เพิ่งส่งเหตุการณ์มา ใช้ replyToken</td><td>ข้อความไม่เกิน 5</td></tr>
<tr><td>Push</td><td><code>POST /v2/bot/message/push</code></td><td>userId / groupId เดียว</td><td>ข้อความไม่เกิน 5</td></tr>
<tr><td>Multicast</td><td><code>POST /v2/bot/message/multicast</code></td><td>userId หลายคน</td><td>ผู้รับไม่เกิน 500, ข้อความไม่เกิน 5</td></tr>
<tr><td>Broadcast</td><td><code>POST /v2/bot/message/broadcast</code></td><td>ทุกคนที่เป็นเพื่อน</td><td>ข้อความไม่เกิน 5</td></tr></table>

<h2>วิธีเลือกใช้ในงานจริง</h2>
<ul>
<li><b>บอตตอบลูกค้า:</b> ใช้ Reply เสมอ เพราะผูกกับบทสนทนาและไม่ต้องรู้ userId ล่วงหน้า</li>
<li><b>แจ้งเตือนออเดอร์/นัดหมาย:</b> ใช้ Push (ต้องมี userId เก็บไว้ตอนลูกค้าเพิ่มเพื่อน)</li>
<li><b>ข่าวถึงกลุ่มที่เลือกไว้:</b> ใช้ Multicast แล้วแบ่งรายชื่อเป็นชุดละ 500</li>
<li><b>ประกาศทั่วไป:</b> Broadcast แต่ควรมีขั้นอนุมัติก่อนเสมอ เพราะส่งแล้วยกเลิกไม่ได้</li>
</ul>

<h2>ตัวอย่างใน n8n (HTTP Request)</h2>
<pre><code>POST https://api.line.me/v2/bot/message/broadcast
Authorization: Bearer {Channel access token}
Content-Type: application/json

{
  "messages": [ { "type": "text", "text": "โปรโมชันวันนี้" } ],
  "notificationDisabled": false
}</code></pre>
<p>ถ้าคำขอ Broadcast อาจถูกลองซ้ำเมื่อเครือข่ายขัดข้อง ข้อกำหนดของ LINE มีส่วนหัว <code>X-Line-Retry-Key</code> สำหรับป้องกันการส่งซ้ำ ให้ตั้งค่าเป็น UUID เดิมเมื่อ retry (อ่านรายละเอียดที่เอกสาร LINE)</p>

<h2>โหนดชุมชนใน n8n</h2>
<p>โหนด <a href="https://github.com/elct9620/n8n-nodes-line-messaging">n8n-nodes-line-messaging</a> รองรับ Reply, Send (Push), Multicast ณ วันที่ตรวจ ยังไม่เห็น Broadcast ในรายการการทำงานของโหนดนี้ ถ้าต้องใช้ ให้ใช้ HTTP Request ตามตัวอย่างด้านบน</p>
<p class="note">ผมไม่ได้ทดสอบกับ channel จริงในบทความนี้ ตัวอย่างทั้งหมดอ้างอิงข้อกำหนดทางการ</p>
""",
    ),
    dict(
        slug="n8n-cloud-or-self-host",
        title="n8n Cloud หรือโฮสต์เอง: เลือกอย่างไร (ราคาปัจจุบันจากหน้าทางการ)",
        desc="เปรียบเทียบ n8n Cloud (Starter €20, Pro €50 ต่อเดือน จ่ายรายปี) กับ Community Edition โฮสต์เอง พร้อมคำถามที่ควรตอบก่อนเลือก ตรวจจากหน้าราคาทางการ",
        faq=[
            ("n8n Cloud ราคาเท่าไร?", "ตามหน้าราคาทางการ (ตรวจ 10 ต.ค. 2026) Starter 20 ยูโรต่อเดือน (จ่ายรายปี) 2,500 workflow executions และ Pro 50 ยูโรต่อเดือน (จ่ายรายปี) 10,000 executions ราคาอาจเปลี่ยน ให้ตรวจหน้า n8n.io/pricing"),
            ("โฮสต์เองฟรีไหม?", "Community Edition ดาวน์โหลดและติดตั้งเองได้โดยไม่มีค่าสมาชิก แต่ต้องรับผิดชอบเซิร์ฟเวอร์ การอัปเดต การสำรองข้อมูล และความปลอดภัยเอง และควรอ่านเงื่อนไขสัญญาอนุญาตก่อนใช้เชิงพาณิชย์"),
            ("ใครควรเริ่มด้วย Cloud?", "คนที่ไม่อยากดูแลเซิร์ฟเวอร์และอยากเริ่มใช้ทันที ส่วนคนที่ต้องการควบคุมข้อมูลหรือมีงานปริมาณมากอาจคุ้มกว่าที่โฮสต์เอง ต้องคำนวณเวลาดูแลด้วย"),
        ],
        body="""
<p><b>คำตอบสั้น:</b> ถ้าอยากเริ่มใช้เร็วและไม่อยากดูแลเซิร์ฟเวอร์ ให้เริ่มที่ <b>n8n Cloud</b> ถ้าต้องการควบคุมข้อมูลเอง ปริมาณงานสูง หรือมีคนดูแลระบบอยู่แล้ว ให้พิจารณา <b>โฮสต์เอง (Community Edition)</b></p>
<p class="note">ตรวจราคาจาก <a href="https://n8n.io/pricing/">หน้าราคาทางการของ n8n</a> เมื่อ {CHECKED} ราคาและเงื่อนไขเปลี่ยนได้ ให้ตรวจที่หน้านั้นก่อนตัดสินใจ</p>

<table><tr><th>แบบ</th><th>ราคาที่หน้าทางการแสดง</th><th>โควตา/ข้อจำกัดที่แสดง</th></tr>
<tr><td>Cloud Starter</td><td>20 ยูโร/เดือน (จ่ายรายปี)</td><td>2,500 workflow executions, รันพร้อมกัน 5, 1 shared project</td></tr>
<tr><td>Cloud Pro</td><td>50 ยูโร/เดือน (จ่ายรายปี)</td><td>10,000 executions, รันพร้อมกัน 50, 3 shared projects</td></tr>
<tr><td>Business</td><td>667 ยูโร/เดือน (จ่ายรายปี)</td><td>40,000 executions, โฮสต์เองเท่านั้น (เวอร์ชัน Cloud อยู่ในรายชื่อรอ)</td></tr>
<tr><td>Community Edition</td><td>ไม่มีค่าสมาชิก</td><td>ติดตั้งเองจาก GitHub ดูแลระบบเอง</td></tr></table>
<p>หน้าราคาระบุว่าจ่ายรายปีประหยัดกว่าจ่ายรายเดือน 17%</p>

<h2>คำถามที่ควรตอบก่อนเลือก</h2>
<ol>
<li><b>มีใครดูแลเซิร์ฟเวอร์ไหม?</b> โฮสต์เอง = อัปเดต สำรองข้อมูล ตรวจความปลอดภัย และตื่นมาแก้เมื่อล่ม</li>
<li><b>workflow รันวันละกี่ครั้ง?</b> Cloud คิดตามจำนวน execution เทียบกับโควตาของแผน</li>
<li><b>ข้อมูลลูกค้าต้องอยู่ที่ไหน?</b> ถ้ามีข้อกำหนดด้านข้อมูลส่วนบุคคล (PDPA) ให้ตรวจเงื่อนไขของผู้ให้บริการและตำแหน่งข้อมูล</li>
<li><b>ต้องการ webhook สาธารณะไหม?</b> บอต LINE ต้องมี URL แบบ HTTPS ที่ LINE เรียกถึง Cloud ให้มาในตัว ส่วนโฮสต์เองต้องตั้งโดเมนหรือท่อ (tunnel)</li>
</ol>
<p class="note">ผมไม่ได้ทดสอบเทียบประสิทธิภาพของสองแบบ บทความนี้เปรียบเทียบจากหน้าราคาและเอกสารทางการเท่านั้น</p>
{AFFILIATE}
""",
    ),
    dict(
        slug="n8n-line-bot-auto-reply",
        title="สร้างบอต LINE ตอบอัตโนมัติด้วย n8n: ตั้งแต่สร้าง channel ถึงตอบกลับ",
        desc="ขั้นตอนทำบอต LINE ตอบข้อความด้วย n8n: สร้าง Messaging API channel ตั้ง webhook ตรวจลายเซ็น อ่านข้อความจาก replyToken แล้วตอบกลับ พร้อมนิพจน์ที่ใช้ได้จริง",
        faq=[
            ("ทำไมต้องตรวจลายเซ็น webhook?", "เพื่อยืนยันว่าคำขอที่เข้ามาส่งจาก LINE จริง LINE ส่งลายเซ็นมาในส่วนหัว x-line-signature ซึ่งคำนวณด้วย HMAC-SHA256 ของเนื้อหาดิบกับ Channel secret แล้วเข้ารหัส base64"),
            ("replyToken ใช้ได้กี่ครั้ง?", "ใช้เพื่อตอบเหตุการณ์นั้นเหตุการณ์เดียวและหมดอายุเร็ว ถ้าต้องส่งภายหลังให้ใช้ Push แทน ตรวจรายละเอียดในเอกสาร LINE"),
            ("ต้องมี URL สาธารณะไหม?", "ต้องมี URL แบบ HTTPS ที่เข้าถึงได้จากอินเทอร์เน็ต เพราะ LINE เรียกเข้ามาที่ webhook ของคุณ"),
        ],
        body="""
<p><b>คำตอบสั้น:</b> บอต LINE ตอบอัตโนมัติด้วย n8n ต้องมี 3 ส่วน: (1) webhook ที่ LINE ส่งเหตุการณ์มา (2) การตรวจว่ามาจาก LINE จริง (3) การตอบกลับด้วย replyToken</p>
<p class="note">ตรวจข้อมูลเมื่อ {CHECKED} จากเอกสารทางการและโค้ดต้นฉบับของโหนดชุมชน <a href="https://github.com/elct9620/n8n-nodes-line-messaging">n8n-nodes-line-messaging</a> ส่วนการตั้งค่าบนหน้าจอ LINE Developers Console อาจเปลี่ยน ผมไม่ได้ทดสอบทั้งขั้นตอนกับ channel จริงในบทความนี้</p>

<h2>ขั้นตอน</h2>
<ol>
<li><b>สร้าง channel:</b> LINE Developers Console → Provider → Messaging API channel เก็บ Channel access token และ Channel secret ใส่ใน Credentials ของ n8n</li>
<li><b>เพิ่มโหนด Line Messaging Trigger</b> เลือกเหตุการณ์ "Message" แล้วคัดลอก URL ของ webhook (แบบ Production) ไปวางที่ช่อง Webhook URL ใน LINE Developers Console แล้วเปิด "Use webhook"</li>
<li><b>ตรวจลายเซ็น:</b> โหนดนี้ตรวจให้เองด้วย Channel secret ตามหลักการคือ HMAC-SHA256 ของเนื้อหาดิบเข้ารหัส base64 เทียบกับส่วนหัว <code>x-line-signature</code> ถ้าคุณทำเองด้วย HTTP/Webhook node ต้องใช้เนื้อหาดิบเท่านั้น</li>
<li><b>เพิ่มโหนด Line Messaging</b> เลือก Operation เป็น Reply แล้วใส่ค่า:
<ul>
<li>Reply Token: <code>{{ $json.replyToken }}</code></li>
<li>Message (Text V2): <code>คุณพิมพ์ว่า: {{ $json.message.text }}</code></li>
</ul></li>
<li><b>ทดสอบ:</b> เพิ่มบัญชีเป็นเพื่อน แล้วพิมพ์ข้อความ ควรได้ข้อความตอบกลับ</li>
</ol>
<p>แต่ละเหตุการณ์ออกมาเป็นหนึ่งรายการ (item) มีฟิลด์ <code>type</code>, <code>replyToken</code>, <code>source</code>, <code>message</code> และ <code>destination</code> ตามโครงสร้างเหตุการณ์ของ LINE</p>

<h2>ข้อผิดพลาดที่พบบ่อย</h2>
<ul>
<li><b>ตอบไม่ได้:</b> replyToken ใช้ได้ครั้งเดียวและหมดอายุเร็ว ให้ตอบทันที ถ้าต้องรอนาน ให้ตอบสั้นๆ ก่อนแล้วใช้ Push ส่งผลทีหลัง</li>
<li><b>webhook ไม่เข้า:</b> ใช้ URL แบบ Test แทน Production หรือ n8n ยังไม่เปิด workflow</li>
<li><b>ลายเซ็นไม่ผ่าน:</b> ใช้ Channel secret ผิดตัว หรือเนื้อหาถูกแก้ก่อนคำนวณ (เช่น จัดรูป JSON ใหม่)</li>
</ul>
<p>ถ้าบอตต้องตอบหลายร้อยคนพร้อมกัน ให้ตรวจโควตาข้อความและขีดจำกัดของแผน n8n ที่ใช้ด้วย (ดู <a href="/guides/n8n-cloud-or-self-host/">n8n Cloud หรือโฮสต์เอง</a>)</p>
""",
    ),
    dict(
        slug="line-rich-menu-api-n8n",
        title="LINE Rich Menu ผ่าน API: สร้าง อัปโหลดรูป ตั้งเมนู (n8n)",
        desc="วิธีสร้าง Rich Menu ของ LINE ด้วย API 3 ขั้น: สร้างเมนู อัปโหลดรูปไปที่ api-data.line.me แล้วตั้งเป็นเมนูตั้งต้นหรือผูกกับผู้ใช้ พร้อม JSON ตัวอย่างและคำขอสำหรับ HTTP Request ใน n8n",
        faq=[
            ("รูป Rich Menu อัปโหลดที่ไหน?", "ต้องอัปโหลดไปที่โฮสต์ api-data.line.me ด้วย POST /v2/bot/richmenu/{richMenuId}/content ไม่ใช่ api.line.me ตามข้อกำหนด OpenAPI ของ LINE และต้องเป็นภาพ JPEG หรือ PNG ที่ขนาดตรงกับ Rich Menu"),
            ("ตั้งเมนูให้ทุกคนหรือรายคนได้ไหม?", "ได้ทั้งสองแบบ: ตั้งเป็นเมนูตั้งต้นของทุกคนด้วย /v2/bot/user/all/richmenu/{richMenuId} หรือผูกกับผู้ใช้รายคนด้วย /v2/bot/user/{userId}/richmenu/{richMenuId}"),
            ("โหนดชุมชนของ n8n มี Rich Menu ไหม?", "ณ วันที่ตรวจ (10 ต.ค. 2026) โค้ดโหนด n8n-nodes-line-messaging ยังไม่มีการทำงานด้าน Rich Menu จึงแนะนำให้ใช้ HTTP Request ตามตัวอย่างในบทความนี้"),
        ],
        body="""
<p><b>คำตอบสั้น:</b> Rich Menu ทำผ่าน API ได้ 3 ขั้น: <b>สร้างเมนู → อัปโหลดรูป → ตั้งให้ใช้</b> ใน n8n ใช้โหนด HTTP Request ได้ทั้งหมด</p>
<p class="note">ตรวจรูปแบบคำขอเมื่อ {CHECKED} จาก <a href="https://github.com/line/line-openapi">ข้อกำหนด OpenAPI ทางการของ LINE</a> ผมยังไม่ได้ทดสอบกับ channel จริงของผู้อ่าน ให้ทดลองบน channel ทดสอบก่อน</p>

<h2>ขั้น 1: สร้างเมนู</h2>
<pre><code>POST https://api.line.me/v2/bot/richmenu
Authorization: Bearer {Channel access token}
Content-Type: application/json

{
  "size": { "width": 2500, "height": 843 },
  "selected": true,
  "name": "เมนูหลัก",
  "chatBarText": "เมนู",
  "areas": [
    {
      "bounds": { "x": 0, "y": 0, "width": 1250, "height": 843 },
      "action": { "type": "message", "text": "สั่งซื้อ" }
    },
    {
      "bounds": { "x": 1250, "y": 0, "width": 1250, "height": 843 },
      "action": { "type": "uri", "uri": "https://example.com" }
    }
  ]
}</code></pre>
<p>ผลลัพธ์จะมี <code>richMenuId</code> ให้เก็บไว้ใช้ขั้นต่อไป ฟิลด์ <code>size, selected, name, chatBarText, areas</code> ตามที่ข้อกำหนดทางการระบุ ขนาดภาพต้องเป็นขนาดที่ LINE รองรับ (เช่น 2500×1686 หรือ 2500×843) ให้ตรวจรายการขนาดในเอกสารล่าสุด</p>

<h2>ขั้น 2: อัปโหลดรูป</h2>
<pre><code>POST https://api-data.line.me/v2/bot/richmenu/{richMenuId}/content
Authorization: Bearer {Channel access token}
Content-Type: image/png        (หรือ image/jpeg)

(เนื้อหาเป็นไบนารีของภาพ)</code></pre>
<p>ใน n8n ตั้ง HTTP Request ให้ส่ง Body เป็น Binary File และกำหนดส่วนหัว Content-Type ให้ตรงกับชนิดภาพ จุดที่พลาดบ่อย: ส่งไปที่ <code>api.line.me</code> แทน <code>api-data.line.me</code></p>

<h2>ขั้น 3: ตั้งให้ใช้</h2>
<ul>
<li><b>ทุกคน:</b> <code>POST https://api.line.me/v2/bot/user/all/richmenu/{richMenuId}</code></li>
<li><b>รายคน:</b> <code>POST https://api.line.me/v2/bot/user/{userId}/richmenu/{richMenuId}</code></li>
<li><b>ถอนจากรายคน:</b> <code>DELETE https://api.line.me/v2/bot/user/{userId}/richmenu</code></li>
</ul>

<h2>คำสั่งที่ใช้บ่อย</h2>
<ul>
<li>ดูรายการ: <code>GET https://api.line.me/v2/bot/richmenu/list</code></li>
<li>ลบเมนู: <code>DELETE https://api.line.me/v2/bot/richmenu/{richMenuId}</code></li>
</ul>

<h2>ใช้กับ n8n อย่างไรให้เป็นระบบ</h2>
<p>ผูกเมนูตามสถานะลูกค้า เช่น ลูกค้าใหม่เห็นเมนูหนึ่ง ลูกค้าที่สั่งแล้วเห็นอีกเมนู โดยให้ workflow เรียกขั้นที่ 3 แบบรายคนเมื่อสถานะเปลี่ยน</p>
<p class="note">ผมกำลังเสนอการทำงานด้าน Rich Menu ให้โหนดชุมชนที่กล่าวถึง (ยังไม่ได้รวมเข้าโปรเจกต์ ณ วันที่เขียน) หากรวมแล้วจะอัปเดตบทความนี้</p>
""",
    ),
]
