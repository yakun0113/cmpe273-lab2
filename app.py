from flask import Flask, escape, request, jsonify
# from flask_restful import Resource, Api

app = Flask(__name__)
# api = Api(app)
# DB = {
#     "students":[],
#     "classes":[]
# }
student_id = 1234456
student_list = {}

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/students', methods=['POST'])
def student():
    global student_id
    global student_list
    content = request.get_json()
    student_name = content["name"]
    student_list[str(student_id)] = student_name
    student_id += 1
    return {"student_id": str(student_id - 1), "name": student_name}, 201

@app.route('/students/<sid>', methods=['GET'])
def get_student(sid):
	global student_list
	return {"id":sid, "name":student_list.get(sid)}

class class_info:
	def __init__(self, course_name):
		self.course_name = course_name
		self.student_list = []


class_id = 1122334
class_list = {}

@app.route('/classes', methods = ['POST'])
def class_name():
	global class_id
	global class_list
	content = request.get_json()
	class_name = content["name"]
	new_class = class_info(class_name)
	class_list[str(class_id)] = new_class
	return{"student_id": str(class_id), "name":new_class.course_name, "students":new_class.student_list}, 201

@app.route('/classes/<cid>', methods = ['GET'])
def get_class_name(cid):
	global class_list
	new_class = class_list.get(cid)
	return {"id": cid, "name": new_class.course_name, "students": new_class.student_list}

@app.route('/classes/<cid>', methods = ['PATCH'])
def add_student(cid):
	global student_id
	global class_id
	global student_list
	global class_list
	content = request.get_json()
	student_id_to_patch = content["student_id"]
	student_name_to_patch = student_list[str(student_id_to_patch)]
	student_info_list = {}
	student_info_list["id"] = student_id_to_patch
	student_info_list["name"] = student_name_to_patch
	class_info = class_list.get(cid)
	class_info.student_list.append(student_info_list)
	return{"id": cid, "name":class_info.course_name, "students":class_info.student_list}, 201


if __name__ == '__main__':
	app.run(debug=True)