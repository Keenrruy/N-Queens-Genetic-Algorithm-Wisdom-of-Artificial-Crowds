import time
import tkinter as tk
from tkinter import ttk

from matplotlib import pyplot as plt

import GAWOCUtil


cell_size = 30
zoom_factor = 1.0
geneticbestpaths = []
geneticbestdistances = []
current_solution_index = 0


def run_genetic_algorithm():
    global geneticbestpaths, geneticbestdistances, exectimes
    geneticbestpaths = []
    geneticbestdistances = []
    exectimes = []
    count_solutions = 0
    tc = 0
    n = int(entry_n.get())
    woc = int(entry_woc.get())
    population_size = int(entry_population.get())
    num_generations = int(entry_generations.get())
    mutation_rate = float(entry_mrate.get())
    for x in range(1):
        start = time.time()
        path, distance, globalbestfitness, globalbestpaths = GAWOCUtil.geneticalgorithmo1woc(n, woc, population_size, num_generations, mutation_rate)
        geneticbestpaths.append(path)
        end = time.time()
        exectime =  end - start
        exectimes.append(exectime)
        geneticbestdistances.append(distance)

    for x in range(len(geneticbestpaths)):
        print(geneticbestdistances[x])

    for y in range(len(exectimes)):
        print(exectimes[y])
    show_current_solution()

    return globalbestfitness, globalbestpaths

def visualize_improvement_curve(globalbestfitness):
    plt.plot(range(1, len(globalbestfitness) + 1), globalbestfitness, marker='o')
    plt.title('Improvement Curve')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid(True)
    plt.show()




def next_solution():
    global current_solution_index
    current_solution_index = min(current_solution_index + 1, len(geneticbestpaths) - 1)
    show_current_solution()


def prev_solution():
    global current_solution_index
    current_solution_index = max(current_solution_index - 1, 0)
    show_current_solution()

def show_current_solution():
    global current_solution_index
    if current_solution_index < len(geneticbestpaths):
        draw_chessboard(int(entry_n.get()), geneticbestpaths[current_solution_index])
        update_info_labels(geneticbestdistances[current_solution_index], exectimes[current_solution_index])
        update_solution_indicator()
    else:
        canvas.delete("all")
        fitness_label.config(text="No more solutions.")
        solution_info_label.config(text="")

def update_solution_indicator():
    global current_solution_index
    solution_info_label.config(text=f"{current_solution_index + 1} of {len(geneticbestpaths)}")


def update_info_labels(distance, execution_time):
    fitness_label.config(text=f"Fitness: {distance:.4f}")
    execution_time_label.config(text=f"Execution Time: {abs(execution_time):.4f} seconds")



def draw_chessboard(board_size, queens_positions):
    scaled_cell_size = cell_size * zoom_factor
    queen_size = int(0.6 * scaled_cell_size)
    canvas.delete("all")
    for i in range(1, board_size + 1):
        for j in range(1, board_size + 1):
            color = "white" if (i + j) % 2 == 0 else "black"
            canvas.create_rectangle((j - 1) * scaled_cell_size, (i - 1) * scaled_cell_size,
                                    j * scaled_cell_size, i * scaled_cell_size,
                                    fill=color)
    for col, row in enumerate(queens_positions):
        canvas.create_text((col + 0.5) * scaled_cell_size, (row - 0.5) * scaled_cell_size,
                           text="♛", font=("Arial", queen_size), fill="red")

def zoom_in():
    global zoom_factor
    zoom_factor *= 1.2  # Increase the zoom factor
    draw_chessboard(int(entry_n.get()), geneticbestpaths[current_solution_index])

def zoom_out():
    global zoom_factor
    zoom_factor /= 1.2  # Decrease the zoom factor
    draw_chessboard(int(entry_n.get()), geneticbestpaths[current_solution_index])


# GUI setup
root = tk.Tk()
root.title("N-Queens Genetic Algorithm")

solution_indicator_label = tk.Label(root, text="Solution: ")

solution_info_label = tk.Label(root, text="1 of 1")
entry_n = tk.Entry(root, width=5)
entry_n.insert(0, "8")
entry_woc = tk.Entry(root, width=5)
entry_woc.insert(0, "100")
entry_population = tk.Entry(root, width=5)
entry_population.insert(0, "20")
entry_generations = tk.Entry(root, width=5)
entry_generations.insert(0, "250")
entry_mrate = tk.Entry(root, width=5)
entry_mrate.insert(0, "0.50")

label_n = tk.Label(root, text="Number of Queens (N):")
label_woc = tk.Label(root, text="Number of Workers (WOC):")
label_population = tk.Label(root, text="Population Size:")
label_generations = tk.Label(root, text="Number of Generations:")
label_mrate = tk.Label(root, text="Mutation Rate:")
fitness_label = tk.Label(root, text="Fitness:")
execution_time_label = tk.Label(root, text="Execution Time: ")

def run_genetic_algorithm_and_visualize():
    globalbestfitness, globalbestpaths = run_genetic_algorithm()
    visualize_improvement_curve(globalbestfitness)


button_run = tk.Button(root, text="Run Genetic Algorithm", command=run_genetic_algorithm_and_visualize)

width = 800
height = 800
canvas_frame = ttk.Frame(root)
canvas_frame.grid(row=0, column=0, rowspan=9, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E))
canvas = tk.Canvas(canvas_frame, width=width, height=height, scrollregion=(0, 0, width*2, height*2))
canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))


x_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
y_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
canvas.config(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
x_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
y_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

label_n.grid(row=0, column=2, sticky="E")
label_woc.grid(row=1, column=2, sticky="E")
label_population.grid(row=2, column=2, sticky="E")
label_generations.grid(row=3, column=2, sticky="E")
label_mrate.grid(row=4, column=2, sticky="E")
entry_n.grid(row=0, column=3)
entry_woc.grid(row=1, column=3)
entry_population.grid(row=2, column=3)
entry_generations.grid(row=3, column=3)
entry_mrate.grid(row=4, column=3)
button_run.grid(row=5, column=2, columnspan=2)
execution_time_label.grid(row=7, column=2, columnspan=2)
fitness_label.grid(row=6, column=2, columnspan=2)


button_zoom_in = tk.Button(root, text="Zoom In", command=zoom_in)
button_zoom_out = tk.Button(root, text="Zoom Out", command=zoom_out)

button_zoom_in.grid(row=8, column=2)
button_zoom_out.grid(row=8, column=3)

button_prev_solution = tk.Button(root, text="Previous Solution", command=prev_solution)
button_next_solution = tk.Button(root, text="Next Solution", command=next_solution)

button_next_solution.grid(row=9, column=3)
button_prev_solution.grid(row=9, column=2)
solution_indicator_label.grid(row=9, column=0, sticky=tk.E)
solution_info_label.grid(row=9, column=1, sticky=tk.W)

root.mainloop()
