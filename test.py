import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Hello World' in r.data.decode('utf-8')


def test_speech():
    import io
    import gspeech
    file_name = 'audio.raw'
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        response = gspeech.process(content)
        assert response.results[0].alternatives[0].transcript == "how old is the Brooklyn Bridge"


def test_speech_request():
    import io
    main.app.testing = True
    client = main.app.test_client()
    r = client.post('/transcribe', data=dict(file=io.open('audio.raw', 'rb')))
    assert r.status_code == 200
    assert "how old is the Brooklyn Bridge" in r.data.decode('utf-8')