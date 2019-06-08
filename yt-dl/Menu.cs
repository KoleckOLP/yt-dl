using System.IO;
using static System.Console;


namespace yt_dl
{
    class Menu
    {
        public void Start()
        {
            Call app = new Call();

            app.Osext();
            app.name = "youtube-dl" + app.ext;

            Clear();
            if (File.Exists(app.name))
            {
                app.name = "ffmpeg" + app.ext;
                if (File.Exists(app.name))
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
                        else if(choice == '9')
                        {
                            app.Chngpath();
                        }
                        else
                        {
                            Clear();
                            WriteLine("choice is 1-6");
                        }
                    }
                }
                else //ffmpeg
                {
                    WriteLine("You are missing ffmpeg, get it here: https://www.ffmpeg.org/");
                    app.Paktq();
                }
            }
            else //youtube-dl
            {
                WriteLine("You are missing youtube-dl, get it here: https://youtube-dl.org/\n" +
                          "Beaware this program breaks youtube TOS section 9.1 https://www.youtube.com/static?template=terms\n" +
                          "Go get it at your own risk.");
                app.Paktq();
            }
            System.Environment.Exit(1);
        }
    }
}