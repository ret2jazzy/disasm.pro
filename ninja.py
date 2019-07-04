from app import asm_ninja, ninja_socketio

if __name__ == '__main__':
    ninja_socketio.run(asm_ninja, port=5000, debug=True)


