from mdscl import main


def test_main_prints_hello(capsys):
    main()

    assert capsys.readouterr().out == "Hello from mdscl!\n"
