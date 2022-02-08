EXPLODER=$1

exploder read $EXPLODER 0 0x100 | grep -v ": 0x00000000"
# 0x100 on: scaler infos
# 0x200-0x203: firmware, serial
# 0x300: key registers (issue DT x, BP y)
# 0x400: sfp status bits
exploder read $EXPLODER 0x1000 0x1000 | grep -v ": 0x00000000"
# 0xf00000: spi self programming (hands off!)
