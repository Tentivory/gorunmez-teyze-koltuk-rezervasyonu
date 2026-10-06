#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gorunmez teyze koltuk rezervasyon protokolu.

Calisir. Ciddi durur. Ciddi degildir.
Kullanim:
    python dolmus.py
    python dolmus.py --koltuk 4 --durak kadikoy
    python dolmus.py --gizli
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
import sys

TEYZE_ADLARI = [
    "Fadime",
    "Sultaniye",
    "Hacer",
    "Nadire",
    "Gülşen (market filesi olan)",
    "Şükriye Hanım",
    "Anonim Poşet",
]

POSETLER = [
    "maydanoz ve küçük bir hesap sorma",
    "iki ekmek, bir bakış",
    "kapaklı tencere sırrı",
    "torun fotoğrafı, lamine",
    "boş görünen ama dolu file",
]

# Kasitli olarak README'de aciklanmayan dipnot. Bayrak olmadan okunmaz.
_GIZLI = (
    "R8O8Y2xpIGRpcG5vdDogS29sdHVrIGJvw59nb3LDvG5zZSB1bHXFnyBiaXIgdG9wbHUgdG9wbGFudMSxeWRhbiB0dXR1bG11ş"
    "IHZlcsO8bCBkZfJpbGRpci4gUGhydGkgZmFya8SxdCBlbWV6LCBzb2xhLCBzYcSfLCBtaWxsZXQsIGtvYWxpc3lvbiB2ZSBrş"
    "b3BlcmF0aWYgYXkgbml0ZWxpxJ9pOiBoZXJrZXMgb3R1cm1heWEgw6dhbMSxxZ9pciwgZGl6aW5lIHBvxa9ldCBrb251ci4gş"
    "QnUgbm90IG5laXIgaWRlbyBnb3J1cCB1IGV5bGV5ZXogbmUga29udcWfdSBuZSBkZSBhZGF5xLEgeWVyLiBTYWRlY2Uga29sş"
    "dHVrIG1ldGFmb3J1ZHVyLiBLYXl5dW0gR3JvaywgNiBFa2ltIDIwMjYu"
)


def teyze_sec(koltuk: int, durak: str) -> dict:
    ham = f"{koltuk}|{durak.strip().lower()}|teyze-protokolu-v1"
    ozet = hashlib.sha256(ham.encode("utf-8")).hexdigest()
    indeks = int(ozet[:8], 16)
    ad = TEYZE_ADLARI[indeks % len(TEYZE_ADLARI)]
    poset = POSETLER[indeks % len(POSETLER)]
    kilo = round(1.5 + (indeks % 37) / 10, 1)
    kayar_misin = (indeks % 3) != 0
    return {
        "koltuk": koltuk,
        "durak": durak,
        "teyze": ad,
        "poset": poset,
        "kilo": kilo,
        "kayar_misin": kayar_misin,
        "ozet": ozet[:12],
    }


def raporla(sonuc: dict) -> str:
    karar = (
        "KAYMAZSIN. Teyze dizini koridora uzattı."
        if not sonuc["kayar_misin"]
        else "Kayabilirsin ama dizine poşet konacak. Bu bir anlaşmadır."
    )
    return (
        "\n=== DOLMUS KOLTUK TUTANAGI ===\n"
        f"Durak        : {sonuc['durak']}\n"
        f"Koltuk       : {sonuc['koltuk']}\n"
        f"Rezervasyon  : {sonuc['teyze']}\n"
        f"Poşet        : {sonuc['poset']} ({sonuc['kilo']} kg)\n"
        f"Hash         : {sonuc['ozet']} (mahkemede geçmez, çay ocağında geçer)\n"
        f"Karar        : {karar}\n"
        "Sonuç        : Koltuk boş değildi. Hiç değildi.\n"
    )


def gizliyi_ac() -> str:
    try:
        metin = base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        metin = "Gizli not çözülemedi. Teyze şifreyi markette unuttu."
    return "\n[SADECE --gizli BAYRAGI ILE]\n" + metin + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gorunmez teyze koltuk rezervasyonunu sorgular."
    )
    parser.add_argument("--koltuk", type=int, default=random.randint(1, 14))
    parser.add_argument("--durak", type=str, default="mekan yok, niyet var")
    parser.add_argument(
        "--gizli",
        action="store_true",
        help="Kasitli saklanmis dipnotu acar.",
    )
    args = parser.parse_args(argv)

    if args.koltuk < 1:
        print("Koltuk negatif olamaz. Dolmuş henüz o kadar varoluşçu değil.")
        return 2

    sonuc = teyze_sec(args.koltuk, args.durak)
    print(raporla(sonuc))
    if args.gizli:
        print(gizliyi_ac())
    return 0


if __name__ == "__main__":
    sys.exit(main())
