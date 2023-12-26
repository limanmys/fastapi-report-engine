# FastAPI Report Engine

[Jinja2](https://palletsprojects.com/p/jinja/) formatında oluşturulmuş .docx uzantılı rapor şablonları kullanılarak özelleştirilmiş PDF ve CSV rapor almayı sağlayan raporlama servisi.

## Kullanım
[Link](https://github.com/limanmys/fastapi-report-engine/releases/latest) üzerinden güncel deb paketi, Ubuntu 20.x ve 22.x sistemlere kurularak kullanılmaya başlanabilir. Sistem üzerinde `report-engine.service` servis adıyla ve `8001` portu üzerinden çalışmaktadır.

```bash
sudo apt install ./report-engine-47.deb
# servis loglarını görüntülemek için
sudo journalctl -u report-engine.service -f
```

## Dokümantasyon
Servis sağlıklı bir şekilde çalışıyorken `<IP_ADDR>:8001/docs` adresi üzerinden Swagger dokümantasyonuna ulaşılabilir.

![swagger.png](./images/swagger.png)