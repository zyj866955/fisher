from app import create_app

app = create_app()
if __name__ == '__main__':
    print(id(app))
    # main函数判断的作用，当作为模块被导入使用的时候，是不执行的，在生产环境中，通过uwgi启动app文件此时便不会执行
    app.run(debug=app.config['DEBUG'], host='0.0.0.0')
