using System;
using System.IO;
using System.Reflection;
using System.Diagnostics;
using static System.Console;

namespace yt_dl
{
    class Menu
    {
        public void Start()
        {
            Call app = new Call();

            app.OS();

            Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName);

            string prog = app.youtubedl.FileName = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName) + app.slash + "youtube-dl" + app.ext;

            app.settings = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName) + app.slash + "settings.json";

            Clear();
            if (File.Exists(prog))
            {
                prog = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName) + app.slash + "ffmpeg" + app.ext;
                if (File.Exists(prog))
                {
                    char choice;

                    app.Update();

                    app.Load();

                    Write("\n");
                    app.Showpath();

                    while (true)
                    {
                        WriteLine("\n1. Audio, " +
                                    "4. Audio playlist\n" +
                                    "2. Video\n" +
                                    "3. Exit\n\n" +
                                    "7. About & Credits\n" +
                                    "8. Show Download path\n" +
                                    "9. Change Download path");
                        Write("#");
                        choice = ReadKey().KeyChar;
                        if (choice == '1')
                        {
                            app.Audio();
                        }
                        else if (choice == '4')
                        {
                            app.PlAudio();
                        }
                        else if (choice == '2')
                        {
                            app.Video();
                        }
                        else if (choice == '3')
                        {
                            break;
                        }
                        else if (choice == '7')
                        {
                            Clear();
                            Call.Help();
                        }
                        else if (choice == '8')
                        {
                            Clear();
                            app.Showpath();
                        }
                        else if (choice == '9')
                        {
                            app.Chngpath();
                        }
                        else if (choice == '`')
                        {
                            app.Debug();
                        }
                        else
                        {
                            Clear();
                            WriteLine("choice is 1-???");
                        }
                    }
                }
                else //ffmpeg
                {
                    WriteLine("You are missing ffmpeg, get it here: https://www.ffmpeg.org/\n" +
                              "Place it in the same folder as yt - dl!!!\n");
                    app.Debug();
                }
            }
            else //youtube-dl
            {
                WriteLine("You are missing youtube-dl, get it here: https://youtube-dl.org/\n" +
                          "Place it in the same folder as yt-dl!!!\n" +
                          "Beaware this program breaks youtube TOS section 9.1 https://www.youtube.com/static?template=terms\n" +
                          "Go get it at your own risk.\n");
                app.Debug();
            }
            System.Environment.Exit(1);
        }
    }
}