#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:09:03 2019
@author: Konrad
"""

import tkinter as tk
import numpy as np
import time

class Bob():
    def __init__(self, canvas, center, length, angle, mass, radius):
        self.length = length
        self.angle = angle
        self.center = center
        self.position = [self.center[0] + xy(self.length, self.angle)[0],
                         self.center[1] + xy(self.length, self.angle)[1]]
        self.mass = mass
        self.radius = radius
        self.ang_vel = 0
        self.ang_acc = 0
        self.canvas = canvas
        self.bob = self.canvas.create_oval(self.dimensions(), fill = "white", outline = "")
        self.rod = self.canvas.create_line(center[0], center[1], self.position, fill = "white")
    def dimensions(self):
        x0, y0 = self.position[0] - self.radius, self.position[1] - self.radius
        x1, y1 = self.position[0] + self.radius, self.position[1] + self.radius
        return [x0, y0, x1, y1]
    def move(self, center):
        self.ang_vel += self.ang_acc
        self.angle += self.ang_vel
        self.position = [center[0] + xy(self.length, self.angle)[0],
                         center[1] + xy(self.length, self.angle)[1]]
        self.canvas.coords(self.bob, self.dimensions())
        self.canvas.coords(self.rod, [center[0], center[1],
                                      self.position[0], self.position[1]])

def xy(length, angle):
    x = length * np.sin(angle)
    y = length * np.cos(angle)
    return [x, y]

def movement(g, bob1, bob2):
    num20 = 2 * np.sin(bob1.angle - bob2.angle)

    num11 = - g * (2 * bob1.mass + bob2.mass) * np.sin(bob1.angle)
    num12 = - bob2.mass * g * np.sin(bob1.angle - 2 * bob2.angle)
    num13 = - num20 * bob2.mass * ((bob2.ang_vel ** 2) * bob2.length + (bob1.ang_vel ** 2) * bob1.length * np.cos(bob1.angle - bob2.angle))
    den1 = bob1.length * (2 * bob1.mass + bob2.mass - bob2.mass * np.cos(2 * (bob1.angle - bob2.angle)))
    bob1.ang_acc = (num11 + num12 + num13) / den1

    num21 = (bob1.ang_vel ** 2) * bob1.length * (bob1.mass + bob2.mass)
    num22 = g * (bob1.mass + bob2.mass) * np.cos(bob1.angle)
    num23 = (bob2.ang_vel ** 2) * bob2.length * bob2.mass * np.cos(bob1.angle - bob2.angle)
    den2 = bob2.length * (2 * bob1.mass + bob2.mass - bob2.mass * np.cos(2 * (bob1.angle - bob2.angle)))
    bob2.ang_acc = num20 * (num21 + num22 + num23) / den2

def tracer(canvas, x, y, ftracer):
    N = len(ftracer) - 1
    ftracer.append(canvas.create_line(x[N - 1], y[N - 1], x[N], y[N], fill = "white"))

def main():
    root = tk.Tk()
    root.title("Double Pendulum")
    window_width, window_height = 500, 500
    window = tk.Canvas(width = window_width, height = window_height,
                       bg = "black", highlightthickness = 0)
    window.pack()

    r0 = 2
    center = [window_width / 2, 2 * window_height / 5]
    bob0 = window.create_oval(center[0] - r0, center[1] - r0,
                              center[0] + r0, center[1] + r0,
                              fill = "white", outline = "")

    l1, a1, m1, r1 = 100, np.pi / 2, 40, 5
    bob1 = Bob(window, center, l1, a1, m1, r1)

    a2 = np.pi / 2
    bob2 = Bob(window, bob1.position, l1, a2, m1, r1)
    tracerx, tracery = [], []
    tracerx.append(bob2.position[0])
    tracery.append(bob2.position[1])
    final_tracer = []

    end_time = []
    n = 0
    start = time.time()
    while True:
        movement(1, bob1, bob2)
        bob1.move(center)
        bob2.move(bob1.position)
        tracerx.append(bob2.position[0])
        tracery.append(bob2.position[1])
        tracer(window, tracerx, tracery, final_tracer)
        end_time.append(time.time())
        display_text = "time elapsed: %s s" % float("%.4g" % (end_time[n] - start))
        time_text = window.create_text([window_width / 2, 5 * window_height / 6],
                                       text = display_text, fill = "white", anchor = "center")
        window.update()
        window.delete(time_text)
        n += 1
    root.mainloop()

main()
