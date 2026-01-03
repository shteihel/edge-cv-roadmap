#!/bin/bash
FILE="system_status.csv"
SIZE=$(du -k "$FILE" | cut -f1)
# du -k: размер в килобайтах
# cut -f1: отрезает имя файла, оставляет только цифру
if [ "$SIZE" -gt 1 ]; then
    # -gt означает "Greater Than" (больше чем)
    echo "Файл большой ($SIZE Kb). Ротация..."
    
    # Генерируем имя с датой (чтобы не затирать старые)
    ARCHIVE_NAME="backup_$(date +%s).tar.gz"
    
    # 1. Архивируем
    tar -czf "$ARCHIVE_NAME" "$FILE"
    
    # 2. Очищаем
    # Этот символ "больше" просто стирает содержимое файла в ноль.
    > "$FILE"
    
    echo "Готово. Создан $ARCHIVE_NAME"
else
    echo "Размер в норме ($SIZE Kb). Пропускаем."
fi