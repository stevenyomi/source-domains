import jmcomic
import newtoki
import toonkor
import wnacg
import zerobyw


def main():
    exceptions = []
    for mod in (jmcomic, newtoki, toonkor, wnacg, zerobyw):
        try:
            mod.main()
        except Exception as e:
            exceptions.append(e)
    if exceptions:
        raise ExceptionGroup("Update failed", exceptions)


main()
