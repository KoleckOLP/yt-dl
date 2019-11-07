using System.IO;
using System.Reflection;
using static System.Console;

namespace yt_dl
{
    class Menu
    {
        public void Start()
        {
            Call app = new Call();

            app.OS();

            if ((File.Exists(app.youtubedl.FileName) && File.Exists(app.ffmpeg.FileName)) && File.Exists(app.ffprobe.FileName))
            {
                    app.indir = true;
            }
            else //youtube-dl & ffmpeg from path
            {
                app.youtubedl.FileName = "youtube-dl" + app.ext;
                app.ffmpeg.FileName = "ffmpeg" + app.ext;
                app.ffprobe.FileName = "ffprobe" + app.ext;

                app.indir = false;

                app.yttest();
            }

            char choice;

            Clear();
            WriteLine("yt-dl {0} by KoleckOLP (C){1}\n", Assembly.GetEntryAssembly().GetName().Version.ToString(), yt_dl.AssemblyInfo.Date.ToString("yyyy"));

            if (File.Exists(app.settings))
            {
                app.Load();

                app.Showpath();
            }
            else
            {
                WriteLine("You have not set a download path do so now.");
                app.Chngpath();
            }

            while (true)
            {
                WriteLine("\n1. Audio\n" +
                          "2. Video\n" +
                          "3. Exit\n" +
                          "4. Subtitles\n\n" +
                          "6. Update youtube-dl\n" +
                          "7. About & Credits\n" +
                          "8. Show Download path\n" +
                          "9. Change Download path");
                Write("#");
                choice = ReadKey().KeyChar;
                if (choice == '1') //Audio
                {
                    app.Audio();
                }
                else if (choice == '4') //Subtitles
                {
                    app.Subtitles();
                }
                else if (choice == '2') //Video
                {
                    app.Video();
                }
                else if (choice == '3') //Exit
                {
                    break;
                }
                else if (choice == '6') //Update youtube-dl
                {
                    app.Update();
                }
                else if (choice == '7') //About
                {
                    Clear();
                    Call.Help();
                }
                else if (choice == '8') //Show download path
                {
                    Clear();
                    app.Showpath();
                }
                else if (choice == '9') //Change download path
                {
                    WriteLine("");
                    app.Chngpath();
                }
                else if (choice == '`') //Debug
                {
                    app.Debug();
                }
                else
                {
                    Clear();
                    WriteLine("choice is 1-???");
                }
            }

            System.Environment.Exit(1);
        }
    }
}