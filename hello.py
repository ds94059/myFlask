from flask import Flask, jsonify, render_template
import subprocess
import time

import rclpy
from std_msgs.msg import String

app = Flask(__name__)

rclpy.init()
flaskNode = rclpy.create_node('flask_publisher')
flaskPub = flaskNode.create_publisher(String, 'rgb_color', 10)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/node")
def nodeList():
    output = open('output.txt', 'w')
    subprocess.call("ros2 node list",
                    shell=True, executable="/bin/bash", stdout=output)

    with open('output.txt', 'r') as output:
        tmp = output.readlines()
        print(tmp)
        return render_template('index.html', node_list=tmp)


@app.route("/color/<color_value>")
def setColor(color_value):
    color_value = "#"+color_value
    print(color_value)
    start = time.time()

    msg = String()
    msg.data = color_value
    flaskPub.publish(msg)

    proc_time = time.time()-start
    print(round(proc_time, 5))
    result = {
        "status": "success"
    }
    return result
