# Endpaper screenshots

The AppStream screenshots in `assets/endpaper/` are taken with made-up sample books (`books.py`: texts and covers drawn for them, no real books), in a window of 1280 × 800 at scale 2.

```bash
python3 shoot.py <out folder> light
python3 shoot.py <out folder> dark
```

Run each in a visible window, floating and without focus, for example with `hyprctl dispatch 'hl.exec_cmd(...)'`; the script expects the Endpaper source in `~/Development/Endpaper`.
