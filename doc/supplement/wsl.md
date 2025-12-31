# สร้าง environment บน WSL

ในกรณีที่ใช้ระบบปฎิบัติการ Windows และไม่ต้องการติดตั้ง Docker desktop อีกวิธีการหนึ่งในการสร้าง environment ที่สามารถใช้เครื่องมือต่างๆ ที่กล่าวถึงในหนังสือนี้ได้คือใช้ WSL (Windows Subsystem for Linux) โดยมีขั้นตอนดังนี้

## 1. ติดตั้ง WSL 

ตามที่แนะนำใน [วีดีโอนี้ (นาที 9.50 - 22.22)](https://youtu.be/FbjwCow3tiI?si=GLvL0EmDqELxLEv6&t=592) แนะนำ Ubuntu 24.04 LTS 

หลังจากนั้นอาจใช้ venv สร้าง environment ตามที่นำเสนอในวีดีโอก็ได้ แต่ในบทความนี้จะใช้ miniconda ซึ่งเป็นวิธีที่สะดวก 

## 2. อัพเดตและอัพเกรด Ubuntu

เปิดหน้าต่าง terminal ของ Ubuntu และพิมพ์คำสั่ง

```console
sudo apt update
sudo apt upgrade
```

## 3. ติดตั้ง miniconda

miniconda เป็นเครื่องมือขนาดเล็กของ conda ที่ใช้พื้นที่การติดตั้งน้อยกว่าตัวเต็ม ใช้ wget เพื่อดาวน์โหลดตัวติดตั้งมาโดยคำสั่งดังนี้

```console
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

```
แล้วใช้ bash รันตัวติดตั้ง

```console
bash Miniconda3-latest-Linux-x86_64.sh
```
ตอบคำถามตามที่ข้อความแนะนำ เช่น [Enter] ,อ่าน license terms, yes, [Enter], yes รอจนจบกระบวนการจะเห็นข้อความ Thank you for installing Miniconda3! 

ปิด terminal และเปิดใหม่เพื่อให้ conda ที่เพิ่งติดตั้งทำงาน

## 4. ติดตั้งไลบรารีที่ต้องใช้บน Ubuntu

แพ็กเกจบางตัวที่ใช้ในหนังสือนี้จะต้องการไลบรารีเสริม ที่หากเราไม่ติดตั้งก่อนอาจเกิด error ขึ้นเมือใช้งาน ดังนั้นจึงควรติดตั้งให้เรียบร้อยเสียก่อน (จะเหมือนๆ กับที่ใส่ใน Dockerfile สำหรับสร้าง Docker image) 

```console
sudo apt install -y apt-utils graphviz libzmq3-dev build-essential gfortran unzip wget libblas-dev liblapack-dev pkg-config libmetis-dev patch libpng-dev libfreetype6-dev git
```

ขั้นตอนที่เหลือคือติดตั้งแพ็กเกจสนับสนุนสำหรับเครื่องมือทั้งหมดที่ใช้ในหนังสือ ในบางคำสั่งอาจมีการซ้ำซ้อนกัน หรือไม่จำเป็น เช่นการติดตั้งแพ็กเกจหนึ่งอาจติดตั้งแพ็กเกจที่ต้องการให้อัตโนมัติ อย่างไรก็ตามคำสั่งทั้งหมดที่ระบุนี้ได้ทดสอบแล้วว่าไม่มีปัญหาอะไรขณะที่เขียนบทความนี้ (ธันวาคม 2568)

## 5. ติดตั้งตัวสนับสนุนสำหรับ Jupyter

```console
conda install -y jupyter
```

**หมายเหตุุ :** ในการรันครั้งแรกจะมี error ขึ้นว่า

```console
To accept these channels' Terms of Service, run the following commands:
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

โดยเราจะต้องรัน 2 คำสั่งนี้เพื่อยอมรับ Terms of Service เสียก่อน หลังจากนั้นจะติดตั้งแพ็กเกจของ conda ได้โดยไม่มีปัญหา

## 6. สร้าง environment ใหม่

สร้าง environment สำหรับติดตั้งเครื่องมือทั้งหมดที่ใช้ในหนังสือนี้ โดยตั้งชื่อ environment ตามต้องการ ในที่นี้จะให้ชื่อว่า ocrl 

```console
conda create -n ocrl
```

หลังจากนั้น activate environment 

```console
conda activate ocrl
```

จะเห็นว่าพร้อมพ์เปลี่ยนจาก (base) เป็น (ocrl) แพ็กเกจต่างๆ ที่เราติดตั้งหลังจากนี้ไม่ว่าจะใช้ conda หรือ pip จะถูกติดตั้งลงบน environment นี้ 

## 7. เลือกติดตั้งแพ็กเกจตามต้องการ

การติดตั้งแพ็กเกจอาจใช้ pip หรือ conda ก็ได้ การติดตั้งผ่าน conda มีข้อดีคือชุมชนจะพยายามตรวจสอบว่าแพ็กเกจทั้งหมดไม่ขัดแย้งกัน (แต่ก็ไม่รับประกันได้โดยสมบูรณ์) แนะนำว่าแพ็กเกจเหล่านี้ควรติดตั้งผ่าน conda โดยใช้คำสั่งตามที่แสดง

```console
conda install -y conda-forge::jupyterlab
conda install -y conda-forge::ipopt
conda install -y conda-forge::cyipopt
conda install -y conda-forge::pyoptsparse
```

ส่วนแพ็กเกจอื่นๆ สามารถติดตั้งได้โดยใช้ pip

```console
pip install --upgrade pip
pip install matplotlib pandas scikit-learn torch torchvision torchaudio control drake jax osqp meshcat pyomo manipulation underactuated
```

หากต้องการตรวจสอบว่าติดตั้งแพ็กเกจอะไรไปแล้วบ้างใช้คำสั่ง

```console
pip list
```

## 8. Register environment

```console
python -m ipykernel install --user --name ocrl --display-name "ocrl"
```

## 9. เริ่มต้นใช้งาน Jupyter

ใช้คำสั่ง 

```console
jupyter lab
```

และ Ctrl-click ลิงก์ที่ปรากฎใน terminal เพื่อใช้งาน Jupyter บนเบราเซอร์

สำหรับระบบไฟล์บน WSL เข้าถึงได้จาก File Explorer บนวินโดวส์ โดยบริเวณล่างสุดจะมีแสดง Linux หากมีหลาย Distro เลือกตัวที่เราทำ env นี้ไว้ เ่ช่น Ubuntu-24.04 เข้าไปที่ไดเรคทอรี home/(ชื่อเครื่องเรา) แล้วสร้าง directory ใหม่ตามต้องการ จะเห็น directory นี้ในหน้าเบราเซอร์ Jupyter lab

### การใช้ VSC

เราสามารถใช้ Visual Studio Code เพื่อเปิด notebook ที่อยู่ใน WSL ได้ แต่ในการรัน จะต้องคลิกที่มุมล่างซ้ายและเลือก Connect to WSL using Distro ... เลือก distro ที่เราทำ environment นี้ไว้ และเลือกชื่อ environment ที่ตั้งชื่อไว้ เช่น ocrl ก็จะสามารถรัน notebook ได้