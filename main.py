from pytest import main


if __name__ == '__main__':
    args = [
        '--alluredir={}'.format('./my_allure_results'),
        '--upload_url={}'.format('http://127.0.0.1:8000/api/script/reports/upload'),
        '--upload_project_id={}'.format(4),
        '--upload_username={}'.format('admin'),
        '--upload_secret={}'.format('8FB6CFB4C8CF11EBB523DCA9048E18C3'),
    ]
    main(args)
