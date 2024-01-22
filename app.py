import xml.etree.ElementTree as ET
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
app = Flask(__name__,static_folder="dist/static", template_folder="dist")
CORS(app, resources={r"*": {"origins": "http://localhost:8080"}})
app.config["UPLOAD_FOLDER"] = "./uploaded_files"
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/protein')
def protein():
    return render_template("index.html")

@app.route("/uploadpdb", methods=["POST"])#pdb file
def uploadfile():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    pdb_data = file.read()  # Read the PDB file content
    return jsonify({'pdbData': pdb_data.decode()})

@app.route('/upload', methods=['POST'])#xml file
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file found"}), 400
    file = request.files['file']
    if file:
        body_id_to_index = {}
        file = request.files['file']
        tree=ET.parse(file)
        root=tree.getroot()
        # 存储pointId1和pointId2的值的数组
        pointId1_values = []
        pointId2_values = []
        bodyId1_values = []
        bodyId2_values = []
        body_count = len(root.find("bodies"))
        point_count=len(root.find("points"))
        bar_count=len(root.find("bars"))
        hinge_count=len(root.find("hinges"))
        body_points = []
        bardata=[]
        largestbodyID=0
        flag=0# 存储 pointID 和 bodyID 的数组
        hin_point_id1 = []
        hin_point_id2 = []
        hin_body_id1 = []
        hin_body_id2 = []
        hingedata=[]
# 遍历每个 <hinge> 元素
        for hinge in root.findall('.//hinge'):
    # 获取 point1Id 和 point2Id 属性值
            point1_id = hinge.get('point1Id')
            point2_id = hinge.get('point2Id')
            hin_point_id1.append(point1_id)
            hin_point_id2.append(point2_id)
    # 获取 <bodies> 元素下的 <body> 元素
            bodies = hinge.find('bodies')
            if bodies is not None:
        # 获取 <body> 元素下的 id1 和 id2 属性值
                body1_id = bodies.find('body[@id1]').get('id1')

        # 获取下一个 <body> 元素下的 id2 属性值
                body2_id = bodies.find('body[@id2]').get('id2')
                hin_body_id1.append(body1_id)
                hin_body_id2.append(body2_id)
        hingedata.append({
            'hin_pointId1_values':  hin_point_id1,
            'hin_pointId2_values':  hin_point_id2,
            'hin_bodyId1_values':  hin_body_id1,
            'hin_bodyId2_values':  hin_body_id2
        })
        # 将获取到的值存入数组
        for body in root.find("bodies"):
            body_id = body.get('id')
            if flag==0:
                flag=1
                largestbodyID=body_id
            # 对于每个 body，找到 point 的数量和它们的 ID
            points = body.findall('pointSet/point')
            point_count1 = len(points)
            point_ids = [point.get('id') for point in points]
            body_points.append({
                'body_id': body_id,
                'point_count': point_count1,
                'point_ids': point_ids
            })
            # Create an empty dictionary to store the mapping
            # Populate the dictionary with body_id to index mapping
            for index, body_info in enumerate(body_points):
                body_id = body_info['body_id']
                body_id_to_index[body_id] = index

        result=[body_count,point_count,bar_count,hinge_count]
        for bar in root.findall('.//bar'):
            pointId1 = bar.get('pointId1')
            pointId2 = bar.get('pointId2')
            bodyId1=bar.get('bodyId1')
            bodyId2=bar.get('bodyId2')
            pointId1_values.append(pointId1)
            pointId2_values.append(pointId2)
            bodyId1_values.append(bodyId1)
            bodyId2_values.append(bodyId2)
        bardata.append({
            'pointId1_values': pointId1_values,
            'pointId2_values': pointId2_values,
            'bodyId1_values': bodyId1_values,
            'bodyId2_values': bodyId2_values
        })

        # 打印结果
        # for body_info in body_points:
        #     print(
        #         f"Body ID: {body_info['body_id']} has {body_info['point_count']} points with the following IDs: {body_info['point_ids']}")
        # file_content_string = file_content.decode('utf-8')
        return jsonify({"content": result,"body": body_points,"body_index": body_id_to_index,"largestbodyID":largestbodyID,"largestbodysize":body_points[0]['point_count'],
                        "bardata_start":bardata[0]['pointId1_values'],"hingedata_start":hingedata[0]['hin_pointId1_values'],
                        "bardata_end":bardata[0]['pointId2_values'],"hingedata_end":hingedata[0]['hin_pointId2_values'],
                        "bardata_body1":bardata[0]['bodyId1_values'],"hingedata_body1":hingedata[0]['hin_bodyId1_values'],"bardata_body2":bardata[0]['bodyId2_values'],
                        "hingedata_body2":hingedata[0]['hin_bodyId2_values']})
    return jsonify({"error": "File upload failed"}), 500


@app.route('/data')
def data():
    return render_template("index.html")
if __name__ == '__main__':
    app.run()

# @app.route('/element')
# def element_table():
#     return render_template("element-table.html")
#
# @app.route('/structure')
# def structure():
#     return render_template("structure.html")
# @app.route('/upload')
# def upload():
#     return render_template("uploadfile.html")
# @app.route('/protein',methods=['POST','GET'])
# def protein():
#     if 'file' not in request.files:
#         return "No file part"
#
#     file = request.files['file']
#
#     if file.filename == '':
#         return "No selected file"
#     if file:
#         file_data = file.read()  # Read the file data
#         filename = file.filename
#         file_extension = filename.rsplit('.', 1)[1].lower()
#         return render_template("protein1.html", file_data=file_data.decode('utf-8'),file_extension=file_extension)
#
# @app.route('/api/data', methods=['GET'])
# def get_data():
#     data = {'message': 'Hello from Flask!'}
#     data=jsonify(data)
#     return data
#



