<!-- Proje Başlığı -->
<br />
<div align="center">
  <h3 align="center">Basit Otonom Sürüş: Engelden Kaçma / Duvar İzleme</h3>

  <p align="center">
    ROS ve Lidar Sensörü Kullanarak FSM Tabanlı Otonom Navigasyon
    <br />
    <br />
  </p>
</div>

<!-- Rozetler (Badges) -->
<div align="center">
  <img src="https://img.shields.io/badge/ROS-Melodic%2FNoetic-22314E?style=for-the-badge&logo=ros&logoColor=white" alt="ROS">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Ubuntu-20.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu">
</div>

<!-- İÇİNDEKİLER -->
<details>
  <summary>İçindekiler</summary>
  <ol>
    <li>
      <a href="#proje-hakkında">Proje Hakkında</a>
      <ul>
        <li><a href="#fsm-yapısı">FSM Yapısı</a></li>
      </ul>
    </li>
    <li>
      <a href="#kurulum-ve-çalıştırma">Kurulum ve Çalıştırma</a>
    </li>
    <li><a href="#kullanılan-parametreler">Kullanılan Parametreler</a></li>
    <li><a href="#video-önizleme">Video Önizleme</a></li>
  </ol>
</details>

## Proje Hakkında

Bu proje, bir mobil robotun (TurtleBot) kapalı bir parkurda engellere çarpmadan ilerlemesini sağlayan otonom bir ROS düğümü (node) içerir. 

Proje, **Sonlu Durum Makinesi (Finite State Machine - FSM)** mimarisi üzerine kurulmuştur. Robot, LIDAR sensöründen (`/scan`) gelen verileri işleyerek çevresindeki engelleri algılar ve duruma göre hareket kararı verir.

### FSM Yapısı

Robotun davranış mantığı aşağıdaki durum diyagramında gösterilmiştir:

```mermaid
graph LR
    A((BAŞLANGIÇ)) --> B{Mesafe Kontrolü}
    B -- Yol Açık --> C[İLERİ SÜR]
    B -- Engel Var (< 1.0m) --> D[DÖNÜŞ YAP]
    B -- Kritik Mesafe (< 0.7m) --> E[KAÇINMA (Geri Git)]
    D -- Engel Devam Ediyor --> D
    D -- Yol Açıldı --> C
    E -- Güvenli Mesafeye Çıktı --> C
