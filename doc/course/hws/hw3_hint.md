## Homework 3 hint

### P1

ในขั้นแรกต้องการให้แยกโค้ดตัวอย่างเป็นส่วนย่อย และใช้ markdown cell อธิบายว่าในแต่ละส่วนของโค้ดทำหน้าที่อะไร หากขาดส่วนนี้จะไม่ได้ 2 คะแนน 

จากโค้ดใน [ตัวอย่างตัวควบคุมทำนายโมเดล (MPC)](https://osqp.org/docs/examples/mpc.html) จะให้เมทริกซ์ Ad, Bd ที่เป็นดีสครีต โดยไม่มีการอ้างอิง และไม่ทราบการนิยามสถานะ เราจะต้องคาดเดาเองโดยใช้การจำลองดูผลตอบสนอง โดยกำหนดตำแหน่งเป้าหมายในแนวแกน x,y,z ทีละแกน และตรวจสอบว่าสถานะใดมีการเปลี่ยนแปลงอย่างไร

อีกวิธีการหนึ่งที่สามารถทำได้คือเปรียบเทียบข้อมูลกับตัวอย่างอื่นที่เราทราบการนิยามสถานะ ตัวอย่างเช่นในบทที่ 6 ของหนังสือ ลองเปรียบเทียบกับ A_tilde, B_tilde ในตัวอย่าง quadrotor จะพบว่ามีโครงสร้างที่คล้ายกัน (แม้ตัวเลขจะแตกต่างกัน) ทำให้เราพอคาดเดาการนิยามสถานะได้ 
รูปที่ 1 แสดงการตรวจสอบบนกระดาษ 

<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/quadrotor_compare.jpeg" width = 700 />

รูปที่ 1 การตรวจสอบเมทริกซ์ Ad, Bd เปรียบเทียบกับ A_tilde, B_tilde ในตัวอย่างบทที่ 6 

ในข้อ P1 นี้เราต้องการกำหนดตำแหน่งลอยตัวสุดท้ายคือ $[2.0, \; 1.0, \; 3.0]$ โดยแนววิถีการบินระหว่างนั้นเป็นอิสระ กราฟทั้งหมดที่ต้องการเป็นดังรููปที่ 2 

<table>
<tr>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/r_step.png" />
</td>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/theta_step.png" />
</td>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/v_step.png" />
</td>
</tr>
<tr>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/w_step.png" />
</td>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/u_step.png" />
</td>
</tr>
</table>

รูปที่ 2 พล็อตที่ต้องการสำหรับโจทย์ข้อ P1

### P2

ในโจทย์ข้อย่อยนี้ ต้องการให้ quadrotor ตามรอยแนววิถีที่เป็นเส้นตรง โดย $x, y, z$ เคลื่อนที่ครั้งละ 0.02, 0.01, 0.03 ต่อรอบ ดัังนั้นรันอัลกอริทึมหาค่าเหมาะที่สุดจำนวน 100 รอบ เพื่อให้ quadrotor เคลื่อนเข้าสู่ค่าสุดท้ายเดียวกับ P1 ในโจทย์นี้เราอาจกำหนดความเร็วเชิงเส้นให้กับสถานะอ้างอิง พล็อตที่ต้องการจะเป็นดังรูปที่ 3 

<table>
<tr>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/r_ramp.png" />
</td>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/theta_ramp.png" />
</td>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/v_ramp.png" />
</td>
</tr>
<tr>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/w_ramp.png" />
</td>
<td>
<img src="https://raw.githubusercontent.com/dewdotninja/ocrl/refs/heads/main/doc/course/hws/figs/u_ramp.png" />
</td>
</tr>
</table>

รูปที่ 2 พล็อตที่ต้องการสำหรับโจทย์ข้อ P2

### P3 

สร้างภาพยนต์การบินของ quadrotor โดยใช้โมเดล meshcat จากบทที่ 6 (หรือจะสร้างเองหรือนำมาจากที่อื่นก็ได้ แต่จะต้องมีลักษณะใกล้เคียงกับ quadrotor ที่พบเห็นปกติ คือมี 4 ใบพัด) 

ขั้นต่ำคือต้องการให้สร้างภาพยนต์สำหรับแนววิถีตาม P2 แต่เราอาจสร้างภาพยนต์สำหรับทั้ง P1 และ P2 เปรียบเทียบกันก็ได้ ทำให้เห็นแนววิถีการบินที่แตกต่างกัน ดังที่บันทึกไว้ใน [วีดีโอนี้](https://youtu.be/K3VlTHZYdpM)
