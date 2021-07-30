def Subs(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.tabWidget.setTabText(2, "*Subs")

        temp = tempfile.mkdtemp() + os.path.sep

        window.sub_output_console.setHtml("")  # clearing the output_console.

        url = window.sub_url_bar.text()

        cmd = [[], []]

        if window.sub_playlist_checkbox.isChecked():
            if window.sub_playlist_bar.text() == "":
                cmd[0] = ["youtube-dl", "-o", f"{temp}%(title)s.%(ext)s", "--yes-playlist", "--write-sub",
                          "--write-auto-sub"]
            else:
                numb = window.sub_playlist_bar.text()
                cmd[0] = ["youtube-dl", "-o", f"{temp}%(title)s.%(ext)s", "--yes-playlist", "--playlist-items",
                          f"{numb}", "--write-sub", "--write-auto-sub"]
        else:
            cmd[0] = ["youtube-dl", "-o", f"{temp}%(title)s.%(ext)s", "--no-playlist", "--write-sub",
                      "--write-auto-sub"]

        cmd[1] = ["--sub-format", "vtt", "--skip-download", f"{url}"]

        lang = None

        if window.sub_lang_checkbox.isChecked():
            lang = window.sub_lang_bar.text()

        floc = [f"--ffmpeg-location", f"{spath}"]
        if window.fdir:
            if lang is not None:
                cmd = cmd[0] + lang + floc + cmd[1]
            else:
                cmd = cmd[0] + floc + cmd[1]
        else:
            if lang is not None:
                cmd = cmd[0] + lang + cmd[1]
            else:
                cmd = cmd[0] + cmd[1]

        if window.sub_cookie_checkbox.isChecked():
            if os.path.exists(spath + "cookies.txt"):
                cmd = cmd + ["--cookies", spath + "cookies.txt"]

        window.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

        window.process_start(cmd, window.sub_output_console)

        subpath = glob.glob(f"{temp}*.vtt")
        os.makedirs(window.settings.Youtubedl.videoDir, exist_ok=True)

        for item in subpath:
            namei = os.path.basename(item)
            namei = namei[:-3]
            newsubpath = f"{window.settings.Youtubedl.videoDir}{namei}srt"  # I don't like this fix to a complain about var type
            if os.path.isfile(newsubpath):
                window.sub_output_console.insertPlainText(f"#yt-dl# file {item} already exists skipping...\n")
            else:
                cmd = ["-i", f"{item}", f"{newsubpath}"]

                floc = [f"{spath + os.path.sep + 'ffmpeg'}", "-hide_banner"]
                if window.fdir:
                    cmd = floc + cmd
                else:
                    cmd = ["ffmpeg", "-hide_banner"] + cmd

                if window.sub_cookie_checkbox.isChecked():
                    if os.path.exists(spath + "cookies.txt"):
                        cmd = cmd + ["--cookies", spath + "cookies.txt"]

                window.sub_output_console.insertPlainText("#yt-dl# starting ffmpeg please wait...\n")

                window.process_start(cmd, window.sub_output_console)

        window.running = False
        window.status("Ready.")
        window.tabWidget.setTabText(2, "Subs")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")


def sub_lang(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.sub_output_console.setHtml("")  # clearing the output_console

        url = window.sub_url_bar.text()
        cmd = ["youtube-dl", "--list-subs", "--no-playlist", f"{url}"]

        if window.sub_cookie_checkbox.isChecked():
            if os.path.exists(spath + "cookies.txt"):
                cmd = cmd + ["--cookies", spath + "cookies.txt"]

        window.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

        window.process_start(cmd, window.sub_output_console)

        window.running = False
        window.status("Ready.")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")