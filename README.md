# Conway's Game of Life

A Python implementation of the famous **Conway's Game of Life**, built with [Pygame](https://pypi.org/project/pygame/).

---

## 📜 Rules of the Game

<img width="680" height="346" alt="Rules-of-Conways-Game-of-Life" src="https://github.com/user-attachments/assets/fa1e0ead-77db-4714-b082-5a6255590d63" />

---

## 🚀 Getting Started

### 1. Install dependencies

Make sure you have Python installed, then install **pygame**:

```bash
pip install pygame
# or
python3 -m pip install pygame
```

### 2. Run the program

```bash
python main.py
```

---

## 🎮 Controls

* **Left Click** → Draw cells
* **Right Click** → Erase cells
* **Space** → Start / Stop simulation
* **i** → Step-by-step mode (advance one generation)
* **r** → Reset screen and stop simulation

---

## ⚙️ Configuration

You can adjust the cell size in the code (line 9 of `main.py`):

```python
CELL_SIZE = 10
```

* A **higher number** → larger cells (fewer cells on screen).
* A **lower number** → smaller cells (more cells on screen).

---

## 📌 Notes

* Optimized to only compute neighbors of black cells → better performance on large grids.
* Lightweight and easy to modify for experimentation.
