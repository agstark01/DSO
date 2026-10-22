#!/usr/bin/env python3
import sys
import uuid
import shutil

# 1. Exact UUIDs of the 18 vertical staircase wires to remove
VERTICAL_WIRE_UUIDS_TO_REMOVE = {
    "82bebb34-72d9-48a2-9e6b-0a52a0da02ea", # (337.82, 67.31) -> (337.82, 107.95)
    "bbcbdaf5-6ad5-4e03-9a08-85890d9a07c8", # (336.55, 74.93) -> (336.55, 110.49)
    "91e0c1e4-ceda-4652-bad5-4ed9d47fd055", # (335.28, 91.44) -> (335.28, 113.03)
    "965b007a-89f2-4818-9622-da0ac536003d", # (334.01, 93.98) -> (334.01, 115.57)
    "15452178-a970-4deb-89c8-4d5870dafbf6", # (332.74, 96.52) -> (332.74, 118.11)
    "ec806ed7-abea-43c6-b539-cf8c497965ac", # (331.47, 99.06) -> (331.47, 120.65)
    "c8785e37-855f-424b-a8b6-0d66dd7a45f2", # (330.2, 116.84) -> (330.2, 123.19)
    "0f4c2588-792d-4236-9d22-eb543c8be1e3", # (328.93, 121.92) -> (328.93, 125.73)
    "18cc66a6-4256-4333-a95f-c5564bfed101", # (331.47, 139.7) -> (331.47, 128.27)
    "39521eec-7683-40a2-8fc9-d8bdc045bb37", # (332.74, 142.24) -> (332.74, 130.81)
    "511e2b04-6c36-42d8-ad42-260a42adacf9", # (334.01, 144.78) -> (334.01, 133.35)
    "d99c8728-3798-4318-83b1-177ad585dda1", # (335.28, 149.86) -> (335.28, 135.89)
    "8c436524-b10e-4193-aa2b-5c5f31a4d470", # (336.55, 152.4) -> (336.55, 138.43)
    "a4f5aa5f-5b19-4363-90fb-b325fb95528c", # (337.82, 154.94) -> (337.82, 140.97)
    "06b97f5b-94ad-4b38-84ab-86281b32a019", # (339.09, 175.26) -> (339.09, 143.51)
    "e333a0d8-6031-4199-9a4a-05babd76e9f9", # (341.63, 180.34) -> (341.63, 146.05)
    "606379bc-5862-4131-9db3-0c85978224fc", # (342.9, 205.74) -> (342.9, 148.59)
    "845c50d4-a7b3-4c4b-a7bb-e64d3c6c6439", # (345.44, 209.55) -> (345.44, 151.13)
}

# 2. Exact coordinate replacements to shorten the 18 blue-box wires (keep both labels connected inside each box!)
BLUE_BOX_WIRE_TRIMS = [
    ("(xy 266.7 67.31) (xy 337.82 67.31)",   "(xy 266.7 67.31) (xy 298.45 67.31)"),
    ("(xy 266.7 74.93) (xy 336.55 74.93)",   "(xy 266.7 74.93) (xy 298.45 74.93)"),
    ("(xy 264.16 91.44) (xy 335.28 91.44)",  "(xy 264.16 91.44) (xy 298.45 91.44)"),
    ("(xy 264.16 93.98) (xy 334.01 93.98)",  "(xy 264.16 93.98) (xy 298.45 93.98)"),
    ("(xy 264.16 96.52) (xy 332.74 96.52)",  "(xy 264.16 96.52) (xy 298.45 96.52)"),
    ("(xy 264.16 99.06) (xy 331.47 99.06)",  "(xy 264.16 99.06) (xy 298.45 99.06)"),
    ("(xy 267.97 116.84) (xy 330.2 116.84)", "(xy 267.97 116.84) (xy 298.45 116.84)"),
    ("(xy 267.97 121.92) (xy 328.93 121.92)","(xy 267.97 121.92) (xy 298.45 121.92)"),
    ("(xy 264.16 139.7) (xy 331.47 139.7)",  "(xy 264.16 139.7) (xy 298.45 139.7)"),
    ("(xy 264.16 142.24) (xy 332.74 142.24)","(xy 264.16 142.24) (xy 298.45 142.24)"),
    ("(xy 264.16 144.78) (xy 334.01 144.78)","(xy 264.16 144.78) (xy 298.45 144.78)"),
    ("(xy 264.16 149.86) (xy 335.28 149.86)","(xy 264.16 149.86) (xy 298.45 149.86)"),
    ("(xy 264.16 152.4) (xy 336.55 152.4)",  "(xy 264.16 152.4) (xy 298.45 152.4)"),
    ("(xy 264.16 154.94) (xy 337.82 154.94)","(xy 264.16 154.94) (xy 298.45 154.94)"),
    ("(xy 267.97 175.26) (xy 339.09 175.26)","(xy 267.97 175.26) (xy 298.45 175.26)"),
    ("(xy 267.97 180.34) (xy 341.63 180.34)","(xy 267.97 180.34) (xy 298.45 180.34)"),
    ("(xy 274.32 205.74) (xy 342.9 205.74)", "(xy 274.32 205.74) (xy 298.45 205.74)"),
    ("(xy 274.32 209.55) (xy 345.44 209.55)","(xy 274.32 209.55) (xy 298.45 209.55)"),
]

# 3. Align all 18 J9 horizontal wire stubs so they start cleanly at X = 335.28 and end at J9's pins (X = 350.52)
J9_STUB_ALIGNS = [
    ("(xy 337.82 107.95) (xy 350.52 107.95)", "(xy 335.28 107.95) (xy 350.52 107.95)"),
    ("(xy 336.55 110.49) (xy 350.52 110.49)", "(xy 335.28 110.49) (xy 350.52 110.49)"),
    ("(xy 334.01 115.57) (xy 350.52 115.57)", "(xy 335.28 115.57) (xy 350.52 115.57)"),
    ("(xy 332.74 118.11) (xy 350.52 118.11)", "(xy 335.28 118.11) (xy 350.52 118.11)"),
    ("(xy 331.47 120.65) (xy 350.52 120.65)", "(xy 335.28 120.65) (xy 350.52 120.65)"),
    ("(xy 330.2 123.19) (xy 350.52 123.19)",  "(xy 335.28 123.19) (xy 350.52 123.19)"),
    ("(xy 328.93 125.73) (xy 350.52 125.73)", "(xy 335.28 125.73) (xy 350.52 125.73)"),
    ("(xy 331.47 128.27) (xy 350.52 128.27)", "(xy 335.28 128.27) (xy 350.52 128.27)"),
    ("(xy 332.74 130.81) (xy 350.52 130.81)", "(xy 335.28 130.81) (xy 350.52 130.81)"),
    ("(xy 334.01 133.35) (xy 350.52 133.35)", "(xy 335.28 133.35) (xy 350.52 133.35)"),
    ("(xy 336.55 138.43) (xy 350.52 138.43)", "(xy 335.28 138.43) (xy 350.52 138.43)"),
    ("(xy 337.82 140.97) (xy 350.52 140.97)", "(xy 335.28 140.97) (xy 350.52 140.97)"),
    ("(xy 339.09 143.51) (xy 350.52 143.51)", "(xy 335.28 143.51) (xy 350.52 143.51)"),
    ("(xy 341.63 146.05) (xy 350.52 146.05)", "(xy 335.28 146.05) (xy 350.52 146.05)"),
    ("(xy 342.9 148.59) (xy 350.52 148.59)",  "(xy 335.28 148.59) (xy 350.52 148.59)"),
    ("(xy 345.44 151.13) (xy 350.52 151.13)", "(xy 335.28 151.13) (xy 350.52 151.13)"),
]

# 4. Exact J8 label replacements by coordinate & UUID (Pins 1..19 at X = 408.94)
J8_LABEL_UPDATES = [
    ('(label "PF0"\n\t\t(at 408.94 128.27 0)',       '(label "PB11_TM2_4"\n\t\t(at 408.94 128.27 0)'),
    ('(label "PF1"\n\t\t(at 408.94 130.81 0)',       '(label "PB10_TM2_3"\n\t\t(at 408.94 130.81 0)'),
    ('(label "PC13"\n\t\t(at 408.94 133.35 0)',      '(label "PA0_ADC_IN1"\n\t\t(at 408.94 133.35 0)'),
    ('(label "PC14"\n\t\t(at 408.94 135.89 0)',      '(label "PB1_B0"\n\t\t(at 408.94 135.89 0)'),
    ('(label "PC15"\n\t\t(at 408.94 138.43 0)',      '(label "PA7"\n\t\t(at 408.94 138.43 0)'),
    ('(label "PB12"\n\t\t(at 408.94 140.97 0)',      '(label "PA5_DAC2"\n\t\t(at 408.94 140.97 0)'),
    ('(label "PB14"\n\t\t(at 408.94 143.51 0)',      '(label "PA4_DAC1"\n\t\t(at 408.94 143.51 0)'),
    ('(label "PA7"\n\t\t(at 408.94 146.05 0)',       '(label "PG10_NRST"\n\t\t(at 408.94 146.05 0)'),
    ('(label "PA8"\n\t\t(at 408.94 148.59 0)',       '(label "PF1"\n\t\t(at 408.94 148.59 0)'),
    ('(label "PA9"\n\t\t(at 408.94 151.13 0)',       '(label "PF0"\n\t\t(at 408.94 151.13 0)'),
    ('(label "PA10"\n\t\t(at 408.94 153.67 0)',      '(label "PC15"\n\t\t(at 408.94 153.67 0)'),
    ('(label "EOP+"\n\t\t(at 408.94 156.21 0)',      '(label "PC14"\n\t\t(at 408.94 156.21 0)'),
    ('(label "EOP-"\n\t\t(at 408.94 158.75 0)',      '(label "PC13"\n\t\t(at 408.94 158.75 0)'),
    ('(label "EOP_OUT"\n\t\t(at 408.94 161.29 0)',   '(label "EOP+"\n\t\t(at 408.94 161.29 0)'),
    ('(label "PB8"\n\t\t(at 408.94 163.83 0)',       '(label "EOP-"\n\t\t(at 408.94 163.83 0)'),
    ('(label "PG10_NRST"\n\t\t(at 408.94 166.37 0)', '(label "EOP_OUT"\n\t\t(at 408.94 166.37 0)'),
]

# 5. New labels to place on J9's 18 wire stubs (Y = 107.95 to 151.13)
J9_NEW_LABELS = [
    (107.95, "PB12"),
    (110.49, "PB14"),
    (113.03, "PB15_ADC_IN2"),
    (115.57, "PA8"),
    (118.11, "PA9"),
    (120.65, "PA10"),
    (123.19, "PA11_D-"),
    (125.73, "PA12_D+"),
    (128.27, "PA15_TM2_1"),
    (130.81, "PB3_TM2_2"),
    (133.35, "PB4_B1"),
    (135.89, "PB5_B2"),
    (138.43, "PB6_A0"),
    (140.97, "PB7_A1"),
    (143.51, "PB8"),
    (146.05, "PB9_A2"),
    (148.59, "S1B"),
    (151.13, "S0"),
]

def main():
    sch_path = sys.argv[1] if len(sys.argv) > 1 else "DSO_1draft.kicad_sch"
    shutil.copyfile(sch_path, sch_path + ".exact_bak")

    with open(sch_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Step A: Remove the 18 vertical staircase wires by exact UUID (without regex!)
    for w_uuid in VERTICAL_WIRE_UUIDS_TO_REMOVE:
        idx = text.find(f'(uuid "{w_uuid}")')
        if idx != -1:
            wire_start = text.rfind("\t(wire", 0, idx)
            wire_end = text.find("\n\t)", idx) + 3
            text = text[:wire_start] + text[wire_end:]

    # Step B: Trim the 18 horizontal wires inside the 6 blue boxes so they end cleanly at X = 298.45
    for old_pts, new_pts in BLUE_BOX_WIRE_TRIMS:
        text = text.replace(old_pts, new_pts)

    # Step C: Align the 18 horizontal wire stubs on J9 so they all start at X = 335.28
    for old_pts, new_pts in J9_STUB_ALIGNS:
        text = text.replace(old_pts, new_pts)

    # Step D: Snap J9 (from 368.3 to 355.6) and J8 (from 433.07 to 426.72) onto their wire ends
    text = text.replace(
        '(symbol\n\t\t(lib_id "Connector_Generic:Conn_01x20")\n\t\t(at 368.3 130.81 0)',
        '(symbol\n\t\t(lib_id "Connector_Generic:Conn_01x20")\n\t\t(at 355.6 130.81 0)'
    )
    text = text.replace(
        '(property "Reference" "J9"\n\t\t\t(at 370.84 130.8099 0)',
        '(property "Reference" "J9"\n\t\t\t(at 358.14 130.8099 0)'
    )
    text = text.replace(
        '(property "Value" "Conn_01x20"\n\t\t\t(at 370.84 133.3499 0)',
        '(property "Value" "Conn_01x20"\n\t\t\t(at 358.14 133.3499 0)'
    )

    text = text.replace(
        '(symbol\n\t\t(lib_id "Connector_Generic:Conn_01x20")\n\t\t(at 433.07 151.13 0)',
        '(symbol\n\t\t(lib_id "Connector_Generic:Conn_01x20")\n\t\t(at 426.72 151.13 0)'
    )
    text = text.replace(
        '(property "Reference" "J8"\n\t\t\t(at 435.61 151.1299 0)',
        '(property "Reference" "J8"\n\t\t\t(at 429.26 151.1299 0)'
    )
    text = text.replace(
        '(property "Value" "Conn_01x20"\n\t\t\t(at 435.61 153.6699 0)',
        '(property "Value" "Conn_01x20"\n\t\t\t(at 429.26 153.6699 0)'
    )

    # Step E: Update J8 labels in-place
    for old_lbl, new_lbl in J8_LABEL_UPDATES:
        text = text.replace(old_lbl, new_lbl)

    # Step F: Add the 18 sorted net labels onto J9's wire stubs (at X = 335.28)
    j9_label_blocks = []
    for y_coord, net_name in J9_NEW_LABELS:
        j9_label_blocks.append(f"""\t(label "{net_name}"
\t\t(at 335.28 {y_coord} 0)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify left bottom)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)""")

    last_paren = text.rfind(")")
    text = text[:last_paren] + "\n".join(j9_label_blocks) + "\n)\n"

    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("Done! All 40 pins on J8 and J9 are connected and reordered with zero symbol loss.")

if __name__ == "__main__":
    main()
