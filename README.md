<br />
<div align="center">
  <h3 align="center">Basit Otonom Sürüş: Engelden Kaçma / Duvar İzleme</h3>

  <p align="center">
    ROS ve Lidar Sensörü Kullanarak FSM Tabanlı Otonom Navigasyon
    <br />
    <br />
  </p>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/ROS-Melodic%2FNoetic-22314E?style=for-the-badge&logo=ros&logoColor=white" alt="ROS">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Ubuntu-20.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu">
</div>

<br/>

<details>
  <summary>📝 İçindekiler</summary>
  <ol>
    <li>
      <a href="#proje-hakkında">Proje Hakkında</a>
      <ul>
        <li><a href="#fsm-yapısı">FSM Yapısı</a></li>
        <li><a href="#kullanılan-topicler">Kullanılan Topic'ler</a></li>
      </ul>
    </li>
    <li>
      <a href="#kurulum-ve-çalıştırma">Kurulum ve Çalıştırma</a>
    </li>
    <li><a href="#kullanılan-parametreler">Kullanılan Parametreler</a></li>
  </ol>
</details>

---

## Proje Hakkında

Bu proje, bir mobil robotun (TurtleBot) kapalı bir parkurda engellere çarpmadan ilerlemesini sağlayan otonom bir ROS düğümü (node) içerir. 

Proje, **Sonlu Durum Makinesi (Finite State Machine - FSM)** mimarisi üzerine kurulmuştur. Robot, LIDAR sensöründen (`/scan`) gelen verileri işleyerek çevresindeki engelleri algılar ve duruma göre hareket kararı verir.

### FSM Yapısı

Robotun davranış mantığı aşağıdaki durum diyagramında gösterilmiştir:

```mermaid
graph LR
    A((BAŞLANGIÇ)) --> B{Mesafe Kontrolü}
    B -- "Yol Açık" --> C[İLERİ SÜR]
    B -- "Engel Var (< 1.0m)" --> D[DÖNÜŞ YAP]
    B -- "Kritik Mesafe (< 0.7m)" --> E["KAÇINMA (Geri Git)"]
    D -- "Engel Devam Ediyor" --> D
    D -- "Yol Açıldı" --> C
    E -- "Güvenli Mesafeye Çıktı" --> C
```

### Kullanılan Topic'ler

Robotun sensör verilerini okumak ve hareket komutları göndermek için kullandığı ROS topicleri şunlardır:

| Topic Adı | Mesaj Tipi | Açıklama |
| :--- | :--- | :--- |
| `/scan` | `sensor_msgs/LaserScan` | Lidar sensöründen gelen mesafe verileri |
| `/mobile_base/commands/velocity` | `geometry_msgs/Twist` | Robota gönderilen hız komutları |
| `~state` | `std_msgs/String` | Debug amaçlı anlık FSM durumu yayını |

---

## Kurulum ve Çalıştırma

Bu projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin.

### 1. Gereksinimler
* ROS (Melodic veya Noetic)
* Python 3
* `geometry_msgs`, `sensor_msgs` paketleri

### 2. İndirme ve Derleme

```bash
cd ~/catkin_ws/src
git clone [https://github.com/AlperenER/simple_autonomous_driving.git](https://github.com/AlperenER/simple_autonomous_driving.git)
cd ..
catkin_make
source devel/setup.bash
```

### 3. Simülasyonu veya Robotu Başlatma

Önce robotun temel sürücülerini ve lidar sensörünü başlatın:

```bash
roslaunch turtlebot_bringup minimal.launch
roslaunch rplidar_ros test_rplidar.launch
```

### 4. Otonom Düğümü Çalıştırma

Görevi başlatmak için oluşturulan Python scriptini çalıştırın:

```bash
rosrun simple_autonomous_driving gorev1_fsm_node.py
```

---

## Kullanılan Parametreler

Robotun davranışını değiştirmek için kod içerisindeki aşağıdaki değişkenler düzenlenebilir:

| Değişken | Değer | Açıklama |
| :--- | :--- | :--- |
| `forward_speed` | 0.15 | Robotun düz sürüş hızı (m/s) |
| `turn_speed` | 0.45 | Dönüş hızı (rad/s) |
| `obstacle_dist` | 1.0 | Engel algılama mesafesi (metre) |
| `critical_dist` | 0.7 | Acil durum kaçınma mesafesi (metre) |
| `blind_spot` | 0.15 | Sensör kör nokta filtresi |

---

<div align="center">
  <p>Geliştirici: <b>Alperen ER</b></p>
  <p>
    <a href="https://github.com/AlperenER">
      <img src="https://img.shields.io/badge/GitHub-Profilim-black?style=flat-square&logo=github" alt="GitHub">
    </a>
  </p>
</div>
