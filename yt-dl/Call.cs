using System;
using System.IO;
using System.Reflection;
using System.Diagnostics;
using System.Runtime.InteropServices;
using static System.Console;
using Newtonsoft.Json;

namespace yt_dl
{
    class Call
    {

        public string path = ""; //download path
        public string url = "";  //url of video
        public string lnk = "";  //final command for youtube-dl
        public string numb = ""; //vid quality

        public string ext = "";  //extencion .exe or nothing
        public string slash = ""; //linux and windows use different slashes
        public string settings = ""; //settings.json location

        public string audiopath; //path for audio
        public string videopath; //path for video

        public static void Help()
        {
            string name = Assembly.GetEntryAssembly().GetName().Name.ToString();
            string ver = Assembly.GetEntryAssembly().GetName().Version.ToString();
            string year = DateTime.Now.Year.ToString();
            string date = yt_dl.AssemblyInfo.Date.ToString("dd.MM.yyyy");

            WriteLine("{0} vesion: {1}git by KoleckOLP, HorseArmored Inc (C){2}\n" +
                      "Built on: {3}, -h, -?, --help to show this message.\n" +
                      "My webpage: https://koleckolp.github.io/\n" +
                      "Project page: https://github.com/KoleckOLP/yt-dl\n" +
                      "youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez\n" +
                      "           (C)2011-{4} youtube-dl developers\n" +
                      "ffmpeg (C)2000-{5} FFmpeg team", name, ver, year, date, year, year);
        }

        public void Debug()
        {
            string console;

            WriteLine("\nPress any key to quit");
            Write(">");
            console = ReadLine();
            if (console == "paths")
            {
                Clear();
                Call.Paths();
            }
        }

        public static void Paths()
        {
            Write("Paths are:\n" +
                      "SingleFile: {0}\n" +
                      "TempLocExt: {1}\n" +
                      "YouRunFrom: {2}\n", Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName), Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), Environment.CurrentDirectory);

            WriteLine("Press any key to quit");
            ReadKey();
            Clear();
        }

        //Musti OS depend
        public void OS()
        {
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux) || RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                this.ext = "";
                this.slash = "/";
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                this.ext = ".exe";
                this.slash = "\\";
            }
        }

        //Save & Load paths
        public void Load()
        {

            string save = File.ReadAllText(this.settings);
            Save sv = JsonConvert.DeserializeObject<Save>(save);
            audiopath = sv.audiopath;
            videopath = sv.videopath;
        }

        public void Save()
        {
            Save sv = new Save();
            sv.audiopath = audiopath;
            sv.videopath = videopath;

            File.WriteAllText(this.settings, JsonConvert.SerializeObject(sv));
        }

        public void Showpath()
        {
            if(audiopath == "")
            {
                WriteLine("audio is saved to: same folder as yt-dl");
            }
            else
            {
                WriteLine("audio is saved to: {0}",audiopath);
            }

            if (videopath == "")
            {
                WriteLine("video is saved to: same folder as yt-dl");
            }
            else
            {
                WriteLine("video is saved to: {0}", videopath);
            }

        }

        public void Chngpath()
        {
            WriteLine("\n\nType path you want to save your audio\n" +
                      "don't forget to type slash after the last folder\n" +
                      "Right now it's {0}\n" +
                      "to save rith next to yt-dl press <Enter>", audiopath);
            Write("#");
            path = ReadLine();
            audiopath = path;
            WriteLine("\nType path you want to save your videos to\n" +
                        "don't forget to type slash after the last folder\n" +
                        "Right now it's {0}\n" +
                        "to save rith next to yt-dl press <Enter>", videopath);
            Write("#");
            path = ReadLine();
            videopath = path;
            Save();
            Load();
            Clear();
            this.Showpath();
        }

        //Youtube-dl & Downloading
        public ProcessStartInfo youtubedl = new ProcessStartInfo
        {
            UseShellExecute = false,
            CreateNoWindow = false,
            Arguments = ""
        };

        public void Update()
        {
            youtubedl.Arguments = "-U";

            using (var process = Process.Start(youtubedl))
            {
                process.WaitForExit();
            }

            if (File.Exists("youtube-dl-updater.bat")) //windows only
            {
                while (true)
                {
                    if (File.Exists("youtube-dl-updater.bat"))
                    {
                        System.Threading.Thread.Sleep(100);
                    }
                    else
                    {
                        break;
                    }
                }
            }
        }

        public void Audio()
        {
            Clear();
            WriteLine("link to audio or 0 to go back");
            Write("#");
            url = ReadLine();
            if (url == "0")
            {
                Clear();
            }
            else
            {
                lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" --no-playlist -x --prefer-ffmpeg --audio-format mp3 \"{1}\"", audiopath, url);
                youtubedl.Arguments = lnk;
                using (var process = System.Diagnostics.Process.Start(youtubedl))
                {
                    process.WaitForExit();
                }
                Write("\a");
            }
        }

        public void PlAudio()
        {
            Clear();
            WriteLine("link to audio playlist or 0 to go back");
            Write("#");
            url = ReadLine();
            if(url == "0")
            {
                Clear();
            }
            else
            {
                WriteLine("Do you want to download the full playlist <Enter>\n" +
                      "or only part of it, folow this example 1-3,7,10-13 or 0 to go back to menu");
                Write("#");
                numb = ReadLine();
                if (numb == "")
                {
                    lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -x --prefer-ffmpeg --audio-format mp3 \"{1}\"", audiopath, url);
                    youtubedl.Arguments = lnk;
                    using (var process = System.Diagnostics.Process.Start(youtubedl))
                    {
                        process.WaitForExit();
                    }
                    Write("\a");
                }
                else if(numb == "0")
                {
                    Clear();
                }
                else
                {
                    lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" --playlist-items {1} -x --prefer-ffmpeg --audio-format mp3 \"{2}\"", audiopath, numb, url);
                    youtubedl.Arguments = lnk;
                    using (var process = System.Diagnostics.Process.Start(youtubedl))
                    {
                        process.WaitForExit();
                    }
                    Write("\a");
                }
            }
        }

        public void Video()
        {
            Clear();
            WriteLine("link to video or 0 to ga back");
            Write("#");
            url = ReadLine();
            if (url == "0")
            {
                Clear();
            }
            else
            {
                lnk = String.Format("-F --no-playlist {0}", url);
                youtubedl.Arguments = lnk;
                using (var process = System.Diagnostics.Process.Start(youtubedl))
                {
                    process.WaitForExit();
                }
                WriteLine("choose video and audio quality by typing numb+numb");
                Write("#");
                numb = ReadLine();
                lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" -f \"{1}\" --no-playlist --prefer-ffmpeg \"{2}\"", videopath, numb, url);
                youtubedl.Arguments = lnk;
                using (var process = System.Diagnostics.Process.Start(youtubedl))
                {
                    process.WaitForExit();
                }
                Write("\a");
            }
        }
    }
}
