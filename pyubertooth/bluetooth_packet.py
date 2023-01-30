"""Copyright 2013 - 2013 Ryan Holeman

This file is part of Project pyubertooth.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; see the file COPYING.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street,
Boston, MA 02110-1301, USA."""

"""
This is a pure python implementation of bluetooth_packet from libbtbb.  It 
serves as library for python applications.  It is currently in its early stages
and based off of the c library libbtbb and some of my ugly POC code 
github.com/hackgnar/lockdown_2013/src/alpha/pyut_alpha.py.

TODO:
    1) replace shit string casting and use struct for binary serialization
    2) port over more functionality from my alpha code
    3) implement more robust UAP features from c libbtbb
    4) more code cleanup/refactor
    5) implement more c libbtbb features
"""

DEFAULT_AC=0xcc7b7268ff614e1b

DEFAULT_CODEWORD=0xb0000002c7820e7e

max_ac_errors=2

MAX_BARKER_ERRORS=1

sw_check_table4 = [
        0x000000000, 0x100000000, 0x200000000, 0x300000000,
        0x185713da9, 0x085713da9, 0x385713da9, 0x285713da9,
        0x30ae27b52, 0x20ae27b52, 0x10ae27b52, 0x00ae27b52,
        0x28f9346fb, 0x38f9346fb, 0x08f9346fb, 0x18f9346fb,
        0x390b5cb0d, 0x290b5cb0d, 0x190b5cb0d, 0x090b5cb0d,
        0x215c4f6a4, 0x315c4f6a4, 0x015c4f6a4, 0x115c4f6a4,
        0x09a57b05f, 0x19a57b05f, 0x29a57b05f, 0x39a57b05f,
        0x11f268df6, 0x01f268df6, 0x31f268df6, 0x21f268df6,
        0x2a41aabb3, 0x3a41aabb3, 0x0a41aabb3, 0x1a41aabb3,
        0x3216b961a, 0x2216b961a, 0x1216b961a, 0x0216b961a,
        0x1aef8d0e1, 0x0aef8d0e1, 0x3aef8d0e1, 0x2aef8d0e1,
        0x02b89ed48, 0x12b89ed48, 0x22b89ed48, 0x32b89ed48,
        0x134af60be, 0x034af60be, 0x334af60be, 0x234af60be,
        0x0b1de5d17, 0x1b1de5d17, 0x2b1de5d17, 0x3b1de5d17,
        0x23e4d1bec, 0x33e4d1bec, 0x03e4d1bec, 0x13e4d1bec,
        0x3bb3c2645, 0x2bb3c2645, 0x1bb3c2645, 0x0bb3c2645,
        0x0cd446acf, 0x1cd446acf, 0x2cd446acf, 0x3cd446acf,
        0x148355766, 0x048355766, 0x348355766, 0x248355766,
        0x3c7a6119d, 0x2c7a6119d, 0x1c7a6119d, 0x0c7a6119d,
        0x242d72c34, 0x342d72c34, 0x042d72c34, 0x142d72c34,
        0x35df1a1c2, 0x25df1a1c2, 0x15df1a1c2, 0x05df1a1c2,
        0x2d8809c6b, 0x3d8809c6b, 0x0d8809c6b, 0x1d8809c6b,
        0x05713da90, 0x15713da90, 0x25713da90, 0x35713da90,
        0x1d262e739, 0x0d262e739, 0x3d262e739, 0x2d262e739,
        0x2695ec17c, 0x3695ec17c, 0x0695ec17c, 0x1695ec17c,
        0x3ec2ffcd5, 0x2ec2ffcd5, 0x1ec2ffcd5, 0x0ec2ffcd5,
        0x163bcba2e, 0x063bcba2e, 0x363bcba2e, 0x263bcba2e,
        0x0e6cd8787, 0x1e6cd8787, 0x2e6cd8787, 0x3e6cd8787,
        0x1f9eb0a71, 0x0f9eb0a71, 0x3f9eb0a71, 0x2f9eb0a71,
        0x07c9a37d8, 0x17c9a37d8, 0x27c9a37d8, 0x37c9a37d8,
        0x2f3097123, 0x3f3097123, 0x0f3097123, 0x1f3097123,
        0x376784c8a, 0x276784c8a, 0x176784c8a, 0x076784c8a,
        0x19a88d59e, 0x09a88d59e, 0x39a88d59e, 0x29a88d59e,
        0x01ff9e837, 0x11ff9e837, 0x21ff9e837, 0x31ff9e837,
        0x2906aaecc, 0x3906aaecc, 0x0906aaecc, 0x1906aaecc,
        0x3151b9365, 0x2151b9365, 0x1151b9365, 0x0151b9365,
        0x20a3d1e93, 0x30a3d1e93, 0x00a3d1e93, 0x10a3d1e93,
        0x38f4c233a, 0x28f4c233a, 0x18f4c233a, 0x08f4c233a,
        0x100df65c1, 0x000df65c1, 0x300df65c1, 0x200df65c1,
        0x085ae5868, 0x185ae5868, 0x285ae5868, 0x385ae5868,
        0x33e927e2d, 0x23e927e2d, 0x13e927e2d, 0x03e927e2d,
        0x2bbe34384, 0x3bbe34384, 0x0bbe34384, 0x1bbe34384,
        0x03470057f, 0x13470057f, 0x23470057f, 0x33470057f,
        0x1b10138d6, 0x0b10138d6, 0x3b10138d6, 0x2b10138d6,
        0x0ae27b520, 0x1ae27b520, 0x2ae27b520, 0x3ae27b520,
        0x12b568889, 0x02b568889, 0x32b568889, 0x22b568889,
        0x3a4c5ce72, 0x2a4c5ce72, 0x1a4c5ce72, 0x0a4c5ce72,
        0x221b4f3db, 0x321b4f3db, 0x021b4f3db, 0x121b4f3db,
        0x157ccbf51, 0x057ccbf51, 0x357ccbf51, 0x257ccbf51,
        0x0d2bd82f8, 0x1d2bd82f8, 0x2d2bd82f8, 0x3d2bd82f8,
        0x25d2ec403, 0x35d2ec403, 0x05d2ec403, 0x15d2ec403,
        0x3d85ff9aa, 0x2d85ff9aa, 0x1d85ff9aa, 0x0d85ff9aa,
        0x2c779745c, 0x3c779745c, 0x0c779745c, 0x1c779745c,
        0x3420849f5, 0x2420849f5, 0x1420849f5, 0x0420849f5,
        0x1cd9b0f0e, 0x0cd9b0f0e, 0x3cd9b0f0e, 0x2cd9b0f0e,
        0x048ea32a7, 0x148ea32a7, 0x248ea32a7, 0x348ea32a7,
        0x3f3d614e2, 0x2f3d614e2, 0x1f3d614e2, 0x0f3d614e2,
        0x276a7294b, 0x376a7294b, 0x076a7294b, 0x176a7294b,
        0x0f9346fb0, 0x1f9346fb0, 0x2f9346fb0, 0x3f9346fb0,
        0x17c455219, 0x07c455219, 0x37c455219, 0x27c455219,
        0x06363dfef, 0x16363dfef, 0x26363dfef, 0x36363dfef,
        0x1e612e246, 0x0e612e246, 0x3e612e246, 0x2e612e246,
        0x36981a4bd, 0x26981a4bd, 0x16981a4bd, 0x06981a4bd,
        0x2ecf09914, 0x3ecf09914, 0x0ecf09914, 0x1ecf09914]

sw_check_table5 = [
        0x000000000, 0x33511ab3c, 0x3ef526bd1, 0x0da43c0ed,
        0x25bd5ea0b, 0x16ec44137, 0x1b48781da, 0x281962ae6,
        0x132dae9bf, 0x207cb4283, 0x2dd88826e, 0x1e8992952,
        0x3690f03b4, 0x05c1ea888, 0x0865d6865, 0x3b34cc359,
        0x265b5d37e, 0x150a47842, 0x18ae7b8af, 0x2bff61393,
        0x03e603975, 0x30b719249, 0x3d13252a4, 0x0e423f998,
        0x3576f3ac1, 0x0627e91fd, 0x0b83d5110, 0x38d2cfa2c,
        0x10cbad0ca, 0x239ab7bf6, 0x2e3e8bb1b, 0x1d6f91027,
        0x14e1a9b55, 0x27b0b3069, 0x2a148f084, 0x194595bb8,
        0x315cf715e, 0x020deda62, 0x0fa9d1a8f, 0x3cf8cb1b3,
        0x07cc072ea, 0x349d1d9d6, 0x39392193b, 0x0a683b207,
        0x2271598e1, 0x1120433dd, 0x1c847f330, 0x2fd56580c,
        0x32baf482b, 0x01ebee317, 0x0c4fd23fa, 0x3f1ec88c6,
        0x1707aa220, 0x2456b091c, 0x29f28c9f1, 0x1aa3962cd,
        0x21975a194, 0x12c640aa8, 0x1f627ca45, 0x2c3366179,
        0x042a04b9f, 0x377b1e0a3, 0x3adf2204e, 0x098e38b72,
        0x29c3536aa, 0x1a9249d96, 0x173675d7b, 0x24676f647,
        0x0c7e0dca1, 0x3f2f1779d, 0x328b2b770, 0x01da31c4c,
        0x3aeefdf15, 0x09bfe7429, 0x041bdb4c4, 0x374ac1ff8,
        0x1f53a351e, 0x2c02b9e22, 0x21a685ecf, 0x12f79f5f3,
        0x0f980e5d4, 0x3cc914ee8, 0x316d28e05, 0x023c32539,
        0x2a2550fdf, 0x19744a4e3, 0x14d07640e, 0x27816cf32,
        0x1cb5a0c6b, 0x2fe4ba757, 0x2240867ba, 0x11119cc86,
        0x3908fe660, 0x0a59e4d5c, 0x07fdd8db1, 0x34acc268d,
        0x3d22fadff, 0x0e73e06c3, 0x03d7dc62e, 0x3086c6d12,
        0x189fa47f4, 0x2bcebecc8, 0x266a82c25, 0x153b98719,
        0x2e0f54440, 0x1d5e4ef7c, 0x10fa72f91, 0x23ab684ad,
        0x0bb20ae4b, 0x38e310577, 0x35472c59a, 0x061636ea6,
        0x1b79a7e81, 0x2828bd5bd, 0x258c81550, 0x16dd9be6c,
        0x3ec4f948a, 0x0d95e3fb6, 0x0031dff5b, 0x3360c5467,
        0x08540973e, 0x3b0513c02, 0x36a12fcef, 0x05f0357d3,
        0x2de957d35, 0x1eb84d609, 0x131c716e4, 0x204d6bdd8,
        0x0bd1b50fd, 0x3880afbc1, 0x352493b2c, 0x067589010,
        0x2e6cebaf6, 0x1d3df11ca, 0x1099cd127, 0x23c8d7a1b,
        0x18fc1b942, 0x2bad0127e, 0x26093d293, 0x1558279af,
        0x3d4145349, 0x0e105f875, 0x03b463898, 0x30e5793a4,
        0x2d8ae8383, 0x1edbf28bf, 0x137fce852, 0x202ed436e,
        0x0837b6988, 0x3b66ac2b4, 0x36c290259, 0x05938a965,
        0x3ea746a3c, 0x0df65c100, 0x0052601ed, 0x33037aad1,
        0x1b1a18037, 0x284b02b0b, 0x25ef3ebe6, 0x16be240da,
        0x1f301cba8, 0x2c6106094, 0x21c53a079, 0x129420b45,
        0x3a8d421a3, 0x09dc58a9f, 0x047864a72, 0x37297e14e,
        0x0c1db2217, 0x3f4ca892b, 0x32e8949c6, 0x01b98e2fa,
        0x29a0ec81c, 0x1af1f6320, 0x1755ca3cd, 0x2404d08f1,
        0x396b418d6, 0x0a3a5b3ea, 0x079e67307, 0x34cf7d83b,
        0x1cd61f2dd, 0x2f87059e1, 0x22233990c, 0x117223230,
        0x2a46ef169, 0x1917f5a55, 0x14b3c9ab8, 0x27e2d3184,
        0x0ffbb1b62, 0x3caaab05e, 0x310e970b3, 0x025f8db8f,
        0x2212e6657, 0x1143fcd6b, 0x1ce7c0d86, 0x2fb6da6ba,
        0x07afb8c5c, 0x34fea2760, 0x395a9e78d, 0x0a0b84cb1,
        0x313f48fe8, 0x026e524d4, 0x0fca6e439, 0x3c9b74f05,
        0x1482165e3, 0x27d30cedf, 0x2a7730e32, 0x19262a50e,
        0x0449bb529, 0x3718a1e15, 0x3abc9def8, 0x09ed875c4,
        0x21f4e5f22, 0x12a5ff41e, 0x1f01c34f3, 0x2c50d9fcf,
        0x176415c96, 0x24350f7aa, 0x299133747, 0x1ac029c7b,
        0x32d94b69d, 0x018851da1, 0x0c2c6dd4c, 0x3f7d77670,
        0x36f34fd02, 0x05a25563e, 0x0806696d3, 0x3b5773def,
        0x134e11709, 0x201f0bc35, 0x2dbb37cd8, 0x1eea2d7e4,
        0x25dee14bd, 0x168ffbf81, 0x1b2bc7f6c, 0x287add450,
        0x0063bfeb6, 0x3332a558a, 0x3e9699567, 0x0dc783e5b,
        0x10a812e7c, 0x23f908540, 0x2e5d345ad, 0x1d0c2ee91,
        0x35154c477, 0x064456f4b, 0x0be06afa6, 0x38b17049a,
        0x0385bc7c3, 0x30d4a6cff, 0x3d709ac12, 0x0e218072e,
        0x2638e2dc8, 0x1569f86f4, 0x18cdc4619, 0x2b9cded25]

sw_check_table6 = [
        0x000000000, 0x17a36a1fa, 0x2f46d43f4, 0x38e5be20e,
        0x06dabba41, 0x1179d1bbb, 0x299c6f9b5, 0x3e3f0584f,
        0x0db577482, 0x1a161d578, 0x22f3a3776, 0x3550c968c,
        0x0b6fccec3, 0x1ccca6f39, 0x242918d37, 0x338a72ccd,
        0x1b6aee904, 0x0cc9848fe, 0x342c3aaf0, 0x238f50b0a,
        0x1db055345, 0x0a133f2bf, 0x32f6810b1, 0x2555eb14b,
        0x16df99d86, 0x017cf3c7c, 0x39994de72, 0x2e3a27f88,
        0x1005227c7, 0x07a64863d, 0x3f43f6433, 0x28e09c5c9,
        0x36d5dd208, 0x2176b73f2, 0x1993091fc, 0x0e3063006,
        0x300f66849, 0x27ac0c9b3, 0x1f49b2bbd, 0x08ead8a47,
        0x3b60aa68a, 0x2cc3c0770, 0x14267e57e, 0x038514484,
        0x3dba11ccb, 0x2a197bd31, 0x12fcc5f3f, 0x055fafec5,
        0x2dbf33b0c, 0x3a1c59af6, 0x02f9e78f8, 0x155a8d902,
        0x2b658814d, 0x3cc6e20b7, 0x04235c2b9, 0x138036343,
        0x200a44f8e, 0x37a92ee74, 0x0f4c90c7a, 0x18effad80,
        0x26d0ff5cf, 0x317395435, 0x09962b63b, 0x1e35417c1,
        0x35fca99b9, 0x225fc3843, 0x1aba7da4d, 0x0d1917bb7,
        0x3326123f8, 0x248578202, 0x1c60c600c, 0x0bc3ac1f6,
        0x3849ded3b, 0x2feab4cc1, 0x170f0aecf, 0x00ac60f35,
        0x3e936577a, 0x29300f680, 0x11d5b148e, 0x0676db574,
        0x2e96470bd, 0x39352d147, 0x01d093349, 0x1673f92b3,
        0x284cfcafc, 0x3fef96b06, 0x070a28908, 0x10a9428f2,
        0x23233043f, 0x34805a5c5, 0x0c65e47cb, 0x1bc68e631,
        0x25f98be7e, 0x325ae1f84, 0x0abf5fd8a, 0x1d1c35c70,
        0x032974bb1, 0x148a1ea4b, 0x2c6fa0845, 0x3bccca9bf,
        0x05f3cf1f0, 0x1250a500a, 0x2ab51b204, 0x3d16713fe,
        0x0e9c03f33, 0x193f69ec9, 0x21dad7cc7, 0x3679bdd3d,
        0x0846b8572, 0x1fe5d2488, 0x27006c686, 0x30a30677c,
        0x18439a2b5, 0x0fe0f034f, 0x37054e141, 0x20a6240bb,
        0x1e99218f4, 0x093a4b90e, 0x31dff5b00, 0x267c9fafa,
        0x15f6ed637, 0x0255877cd, 0x3ab0395c3, 0x2d1353439,
        0x132c56c76, 0x048f3cd8c, 0x3c6a82f82, 0x2bc9e8e78,
        0x33ae40edb, 0x240d2af21, 0x1ce894d2f, 0x0b4bfecd5,
        0x3574fb49a, 0x22d791560, 0x1a322f76e, 0x0d9145694,
        0x3e1b37a59, 0x29b85dba3, 0x115de39ad, 0x06fe89857,
        0x38c18c018, 0x2f62e61e2, 0x1787583ec, 0x002432216,
        0x28c4ae7df, 0x3f67c4625, 0x07827a42b, 0x1021105d1,
        0x2e1e15d9e, 0x39bd7fc64, 0x0158c1e6a, 0x16fbabf90,
        0x2571d935d, 0x32d2b32a7, 0x0a370d0a9, 0x1d9467153,
        0x23ab6291c, 0x3408088e6, 0x0cedb6ae8, 0x1b4edcb12,
        0x057b9dcd3, 0x12d8f7d29, 0x2a3d49f27, 0x3d9e23edd,
        0x03a126692, 0x14024c768, 0x2ce7f2566, 0x3b449849c,
        0x08ceea851, 0x1f6d809ab, 0x27883eba5, 0x302b54a5f,
        0x0e1451210, 0x19b73b3ea, 0x2152851e4, 0x36f1ef01e,
        0x1e11735d7, 0x09b21942d, 0x3157a7623, 0x26f4cd7d9,
        0x18cbc8f96, 0x0f68a2e6c, 0x378d1cc62, 0x202e76d98,
        0x13a404155, 0x04076e0af, 0x3ce2d02a1, 0x2b41ba35b,
        0x157ebfb14, 0x02ddd5aee, 0x3a386b8e0, 0x2d9b0191a,
        0x0652e9762, 0x11f183698, 0x29143d496, 0x3eb75756c,
        0x008852d23, 0x172b38cd9, 0x2fce86ed7, 0x386decf2d,
        0x0be79e3e0, 0x1c44f421a, 0x24a14a014, 0x3302201ee,
        0x0d3d259a1, 0x1a9e4f85b, 0x227bf1a55, 0x35d89bbaf,
        0x1d3807e66, 0x0a9b6df9c, 0x327ed3d92, 0x25ddb9c68,
        0x1be2bc427, 0x0c41d65dd, 0x34a4687d3, 0x230702629,
        0x108d70ae4, 0x072e1ab1e, 0x3fcba4910, 0x2868ce8ea,
        0x1657cb0a5, 0x01f4a115f, 0x39111f351, 0x2eb2752ab,
        0x30873456a, 0x27245e490, 0x1fc1e069e, 0x08628a764,
        0x365d8ff2b, 0x21fee5ed1, 0x191b5bcdf, 0x0eb831d25,
        0x3d32431e8, 0x2a9129012, 0x12749721c, 0x05d7fd3e6,
        0x3be8f8ba9, 0x2c4b92a53, 0x14ae2c85d, 0x030d469a7,
        0x2beddac6e, 0x3c4eb0d94, 0x04ab0ef9a, 0x130864e60,
        0x2d376162f, 0x3a940b7d5, 0x0271b55db, 0x15d2df421,
        0x2658ad8ec, 0x31fbc7916, 0x091e79b18, 0x1ebd13ae2,
        0x2082162ad, 0x37217c357, 0x0fc4c2159, 0x1867a80a3];

sw_check_table7 = [
        0x000000000, 0x3f0b9201f, 0x264037d97, 0x194ba5d88,
        0x14d77c687, 0x2bdcee698, 0x32974bb10, 0x0d9cd9b0f,
        0x29aef8d0e, 0x16a56ad11, 0x0feecf099, 0x30e55d086,
        0x3d7984b89, 0x027216b96, 0x1b39b361e, 0x243221601,
        0x0b0ae27b5, 0x3401707aa, 0x2d4ad5a22, 0x124147a3d,
        0x1fdd9e132, 0x20d60c12d, 0x399da9ca5, 0x06963bcba,
        0x22a41aabb, 0x1daf88aa4, 0x04e42d72c, 0x3befbf733,
        0x367366c3c, 0x0978f4c23, 0x1033511ab, 0x2f38c31b4,
        0x1615c4f6a, 0x291e56f75, 0x3055f32fd, 0x0f5e612e2,
        0x02c2b89ed, 0x3dc92a9f2, 0x24828f47a, 0x1b891d465,
        0x3fbb3c264, 0x00b0ae27b, 0x19fb0bff3, 0x26f099fec,
        0x2b6c404e3, 0x1467d24fc, 0x0d2c77974, 0x3227e596b,
        0x1d1f268df, 0x2214b48c0, 0x3b5f11548, 0x045483557,
        0x09c85ae58, 0x36c3c8e47, 0x2f886d3cf, 0x1083ff3d0,
        0x34b1de5d1, 0x0bba4c5ce, 0x12f1e9846, 0x2dfa7b859,
        0x2066a2356, 0x1f6d30349, 0x062695ec1, 0x392d07ede,
        0x2c2b89ed4, 0x13201becb, 0x0a6bbe343, 0x35602c35c,
        0x38fcf5853, 0x07f76784c, 0x1ebcc25c4, 0x21b7505db,
        0x0585713da, 0x3a8ee33c5, 0x23c546e4d, 0x1cced4e52,
        0x11520d55d, 0x2e599f542, 0x37123a8ca, 0x0819a88d5,
        0x27216b961, 0x182af997e, 0x01615c4f6, 0x3e6ace4e9,
        0x33f617fe6, 0x0cfd85ff9, 0x15b620271, 0x2abdb226e,
        0x0e8f9346f, 0x318401470, 0x28cfa49f8, 0x17c4369e7,
        0x1a58ef2e8, 0x25537d2f7, 0x3c18d8f7f, 0x03134af60,
        0x3a3e4d1be, 0x0535df1a1, 0x1c7e7ac29, 0x2375e8c36,
        0x2ee931739, 0x11e2a3726, 0x08a906aae, 0x37a294ab1,
        0x1390b5cb0, 0x2c9b27caf, 0x35d082127, 0x0adb10138,
        0x0747c9a37, 0x384c5ba28, 0x2107fe7a0, 0x1e0c6c7bf,
        0x3134af60b, 0x0e3f3d614, 0x177498b9c, 0x287f0ab83,
        0x25e3d308c, 0x1ae841093, 0x03a3e4d1b, 0x3ca876d04,
        0x189a57b05, 0x2791c5b1a, 0x3eda60692, 0x01d1f268d,
        0x0c4d2bd82, 0x3346b9d9d, 0x2a0d1c015, 0x15068e00a,
        0x000000001, 0x3f0b9201e, 0x264037d96, 0x194ba5d89,
        0x14d77c686, 0x2bdcee699, 0x32974bb11, 0x0d9cd9b0e,
        0x29aef8d0f, 0x16a56ad10, 0x0feecf098, 0x30e55d087,
        0x3d7984b88, 0x027216b97, 0x1b39b361f, 0x243221600,
        0x0b0ae27b4, 0x3401707ab, 0x2d4ad5a23, 0x124147a3c,
        0x1fdd9e133, 0x20d60c12c, 0x399da9ca4, 0x06963bcbb,
        0x22a41aaba, 0x1daf88aa5, 0x04e42d72d, 0x3befbf732,
        0x367366c3d, 0x0978f4c22, 0x1033511aa, 0x2f38c31b5,
        0x1615c4f6b, 0x291e56f74, 0x3055f32fc, 0x0f5e612e3,
        0x02c2b89ec, 0x3dc92a9f3, 0x24828f47b, 0x1b891d464,
        0x3fbb3c265, 0x00b0ae27a, 0x19fb0bff2, 0x26f099fed,
        0x2b6c404e2, 0x1467d24fd, 0x0d2c77975, 0x3227e596a,
        0x1d1f268de, 0x2214b48c1, 0x3b5f11549, 0x045483556,
        0x09c85ae59, 0x36c3c8e46, 0x2f886d3ce, 0x1083ff3d1,
        0x34b1de5d0, 0x0bba4c5cf, 0x12f1e9847, 0x2dfa7b858,
        0x2066a2357, 0x1f6d30348, 0x062695ec0, 0x392d07edf,
        0x2c2b89ed5, 0x13201beca, 0x0a6bbe342, 0x35602c35d,
        0x38fcf5852, 0x07f76784d, 0x1ebcc25c5, 0x21b7505da,
        0x0585713db, 0x3a8ee33c4, 0x23c546e4c, 0x1cced4e53,
        0x11520d55c, 0x2e599f543, 0x37123a8cb, 0x0819a88d4,
        0x27216b960, 0x182af997f, 0x01615c4f7, 0x3e6ace4e8,
        0x33f617fe7, 0x0cfd85ff8, 0x15b620270, 0x2abdb226f,
        0x0e8f9346e, 0x318401471, 0x28cfa49f9, 0x17c4369e6,
        0x1a58ef2e9, 0x25537d2f6, 0x3c18d8f7e, 0x03134af61,
        0x3a3e4d1bf, 0x0535df1a0, 0x1c7e7ac28, 0x2375e8c37,
        0x2ee931738, 0x11e2a3727, 0x08a906aaf, 0x37a294ab0,
        0x1390b5cb1, 0x2c9b27cae, 0x35d082126, 0x0adb10139,
        0x0747c9a36, 0x384c5ba29, 0x2107fe7a1, 0x1e0c6c7be,
        0x3134af60a, 0x0e3f3d615, 0x177498b9d, 0x287f0ab82,
        0x25e3d308d, 0x1ae841092, 0x03a3e4d1a, 0x3ca876d05,
        0x189a57b04, 0x2791c5b1b, 0x3eda60693, 0x01d1f268c,
        0x0c4d2bd83, 0x3346b9d9c, 0x2a0d1c014, 0x15068e00b]

#128 values for barker distances
BARKER_DISTANCE = [
        3,3,3,2,3,2,2,1,2,3,3,3,3,3,3,2,2,3,3,3,3,3,3,2,1,2,2,3,2,3,3,3,
        3,2,2,1,2,1,1,0,3,3,3,2,3,2,2,1,3,3,3,2,3,2,2,1,2,3,3,3,3,3,3,2,
        2,3,3,3,3,3,3,2,1,2,2,3,2,3,3,3,1,2,2,3,2,3,3,3,0,1,1,2,1,2,2,3,
        3,3,3,2,3,2,2,1,2,3,3,3,3,3,3,2,2,3,3,3,3,3,3,2,1,2,2,3,2,3,3,3
        ]

barker_correct = [
        '0xb000000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0xb000000000000000',
        '0xb000000000000000', '0xb000000000000000', '0x4e00000000000000',
        '0xb000000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0xb000000000000000', '0xb000000000000000',
        '0xb000000000000000', '0x4e00000000000000', '0xb000000000000000', 
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0xb000000000000000', '0x4e00000000000000', 
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0xb000000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0xb000000000000000',
        '0xb000000000000000', '0xb000000000000000', '0x4e00000000000000',
        '0xb000000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0x4e00000000000000', '0xb000000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0x4e00000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000',
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0x4e00000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000',
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000',
        '0xb000000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000', 
        '0x4e00000000000000', '0x4e00000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0xb000000000000000', '0x4e00000000000000',
        '0xb000000000000000', '0x4e00000000000000', '0x4e00000000000000', 
        '0x4e00000000000000', '0xb000000000000000', '0xb000000000000000',
        '0xb000000000000000', '0x4e00000000000000', '0xb000000000000000',
        '0x4e00000000000000', '0x4e00000000000000', '0x4e00000000000000',
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000',
        '0xb000000000000000', '0xb000000000000000', '0xb000000000000000', 
        '0xb000000000000000', '0x4e00000000000000']

INDICES = [99, 85, 17, 50, 102, 58, 108, 45, 92, 62, 32, 118, 88, 11, 80, 2,
        37, 69, 55, 8, 20, 40, 74, 114, 15, 106, 30, 78, 53, 72, 28, 26, 68, 7,
        39, 113, 105, 77, 71, 25, 84, 49, 57, 44, 61, 117, 10, 1, 123, 124, 22,
        125, 111, 23, 42, 126, 6, 112, 76, 24, 48, 43, 116, 0]

WHITENING_DATA = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0,
        1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1,
        1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0,
        1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0,
        1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]

TYPE_NAMES = ["NULL", "POLL", "FHS", "DM1", "DH1/2-DH1", "HV1", "HV2/2-EV3",
        "HV3/EV3/3-EV3", "DV/3-DH1", "AUX1", "DM3/2-DH3", "DH3/3-DH3",
        "EV4/2-EV5", "EV5/3-EV5", "DM5/2-DH5", "DH5/3-DH5"]

pn = '0x83848D96BBCC54FC'


syndrome_map = {}

def gen_syndrome(codeword):
    syndrome = codeword & int('0xffffffff', 16)
    codeword >>= 32
    syndrome ^= sw_check_table4[codeword & int('0xff', 16)]
    codeword >>= 8
    syndrome ^= sw_check_table5[codeword & int('0xff', 16)]
    codeword >>= 8
    syndrome ^= sw_check_table6[codeword & int('0xff', 16)]
    codeword >>= 8
    syndrome ^= sw_check_table7[codeword & int('0xff', 16)]
    return syndrome
 

def cycle(error, start, depth, codeword):
    #print("cycle ran")
    i = start
    base = 1
    depth -= 1;
    while i < 58:
        new_error = (base << i)
        new_error |= error
        if depth:
            cycle(new_error, i+1, depth, codeword)
        else:
            syndrome = gen_syndrome(codeword ^ new_error)
            syndrome_map[syndrome] = new_error
        i += 1

def gen_syndrome_map(bit_errors):
    i = 1
    while i <= bit_errors:
        cycle(0,0,i,DEFAULT_AC)
        i += 1

gen_syndrome_map(max_ac_errors)

class BtbbPacket(object):

    def __init__(self, data=None):
        self._fields = ["refcount", "flags", "channel", "UAP", "NAP", "LAP",
                "packet_type", "packet_lt_addr", "packet_flags", "packet_hec",
                "packet_header", "payload_header_length", "payload_header",
                "payload_llid", "payload_flow", "payload_length", "payload",
                "crc", "clock", "clkn", "ac_errors", "length", "symbols"]
        for field in self._fields:
            setattr(self, field, None)

        if data:
            self._init_with_data(data)

    def _init_with_data(self, data):
        #TODO: change this to a BitVector. I was in a rush for lockdown con.
        self.channel = data[2]
        self.air_bits = []
        for item in data:
            tmp = bin(item)[2:].zfill(8)
            for i in tmp:
                self.air_bits.append(i)
        self.barker = self.btbb_find_ac(data[7])
        self.detect_lap()
   
   
    @staticmethod    
    def count_bits(n):
        foo = bin(n)[2:]
        return foo.count('1')
   
    @staticmethod    
    def btbb_find_ac(byte):
        """not the best implementation, only looks at one rx data bank, does
        not match ut c libs for all rx data banks.  Does match on ut c libs lap
        hits when compairing nanoseconds. This implementation also has a direct
        corilation with rx packet where ut c lib sends symbs/symbols.
        
        Also, I am consuming a byte here.  This was from my old ugly code"""
        barker = bin(byte)[2:].zfill(8)[1:7]
        barker = int(''.join(list(barker)[::-1]), 2)
        return barker
    
    def detect_lap(self):
        barker = self.barker
        barker <<= 1
        # if we append other symbol bank we dont need to subtract 63...
        #for i in range(400 ):
        for i in range(400 - 63):
            barker >>= 1
            some_bit = int(self.air_bits[63 + i]) << 6
            barker |= some_bit
            if BARKER_DISTANCE[barker] <= MAX_BARKER_ERRORS:
                """next 2 lines replace UT C method air_to_host_64.
                    we do want to totaly fip 64 consecutive bits."""
                syncword = self.air_bits[i:i+64]
                syncword.reverse()
                syncword = int(''.join(syncword), 2)
                corrected_barker = int(barker_correct[syncword >> 57], 16)
                syncword = syncword & int('0x01ffffffffffffff', 16) | \
                        corrected_barker
                codeword = syncword ^ int(pn, 16)
                syndrome = gen_syndrome(codeword) 
                ac_errors=0
                if (syndrome):
                    errors = syndrome_map.get(syndrome, None)
                    if errors != None:
                        syncword ^= errors
                        ac_errors = self.count_bits(errors)
                        syndrome = 0
                    else:
                        ac_errors = 0xff
                    if ac_errors <= max_ac_errors:
                        lap = (syncword >> 34) & 0xffffff
                        lap = hex(lap)[2:]
                        lap = lap.replace('L','').zfill(6)
                        self.LAP=lap
                        offset = i
                        break

    def to_dict(self):
        return dict((f,getattr(self,f)) for f in self._fields)

    def __str__(self):
        #return str(self.to_dict())
        return str(dict((k,v) for k,v in self.to_dict().iteritems() if v is not None))

