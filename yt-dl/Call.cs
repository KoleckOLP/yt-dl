using System;
using System.IO;
using System.Reflection;
using System.Diagnostics;
using System.Runtime.InteropServices;
using Newtonsoft.Json;
using static System.Console;


namespace yt_dl
{
    class Call
    {

        public string path = ""; //download path
        public string url = "";  //url of video
        public string lnk = "";  //final command for youtube-dl
        public string numb = ""; //vid quality
        public string qual = "";

        public bool indir = false; //youtube-dl & ffmpeg local or nah
        public string ext = "";  //extencion .exe or nothing
        public string slash = ""; //linux and windows use different slashes
        public string settings = ""; //settings.json location

        public string audiopath; //path for audio
        public string videopath; //path for video

        public static void Help()
        {
            string ver = Assembly.GetEntryAssembly().GetName().Version.ToString();
            string year = DateTime.Now.Year.ToString();
            string date = yt_dl.AssemblyInfo.Date.ToString("dd.MM.yyyy");

            WriteLine("yt-dl vesion: {0}git by KoleckOLP, HorseArmored Inc (C){1}\n" +
                      "Built on: {2}, -h, -?, --help to show this message.\n" +
                      "My webpage: https://koleckolp.github.io/\n" +
                      "Project page: https://github.com/KoleckOLP/yt-dl\n" +
                      "youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez\n" +
                      "           (C)2011-{3} youtube-dl developers\n" +
                      "ffmpeg (C)2000-{4} FFmpeg team", ver, year, date, year, year);
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

            path = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName);

            youtubedl.FileName = path + slash + "youtube-dl" + ext;
            ffmpeg.FileName = path + slash + "ffmpeg" + ext;
            ffprobe.FileName = path + slash + "ffprobe" + ext;
            settings = path + slash + "settings.json";
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
            WriteLine("audio is saved to: {0}", audiopath); 
            WriteLine("video is saved to: {0}", videopath);
        }

        public void Chngpath()
        {
            string choice = "";

            WriteLine("\nType path you want to save your audio\n" +
                      "Right now it's {0}\n" +
                      "to save right next to yt-dl press <Enter>", audiopath);
            Write("#");
            choice = ReadLine();
            if (choice == "")
            {
                audiopath = path + slash;
            }
            else 
            {
                audiopath = choice + slash;
            }
            WriteLine("\nType path you want to save your videos to\n" +
                        "Right now it's {0}\n" +
                        "to save right next to yt-dl press <Enter>", videopath);
            Write("#");
            choice = ReadLine();
            if (choice == "")
            {
                videopath = path + slash;
            }
            else
            {
                videopath = choice + slash;
            }
            Save();
            Load();
            Clear();
            this.Showpath();
        }

        //Youtube-dl & Downloading
        public ProcessStartInfo youtubedl = new ProcessStartInfo
        {
            WindowStyle = ProcessWindowStyle.Normal,
            RedirectStandardOutput = false,
            RedirectStandardError = false,
            CreateNoWindow = false
        };


        public ProcessStartInfo ffmpeg = new ProcessStartInfo
        {
            WindowStyle = ProcessWindowStyle.Normal,
            RedirectStandardOutput = false,
            RedirectStandardError = false,
            CreateNoWindow = false
        };

        public ProcessStartInfo ffprobe = new ProcessStartInfo
        {
            WindowStyle = ProcessWindowStyle.Normal,
            RedirectStandardOutput = false,
            RedirectStandardError = false,
            CreateNoWindow = false
        };

        public void yttest()
        {
            try
            {
                youtubedl.WindowStyle = ProcessWindowStyle.Hidden;
                youtubedl.RedirectStandardOutput = true;
                youtubedl.RedirectStandardError = true;
                youtubedl.UseShellExecute = false;
                youtubedl.CreateNoWindow = true;
                Process.Start(youtubedl);
                youtubedl.WindowStyle = ProcessWindowStyle.Normal;
                youtubedl.RedirectStandardOutput = false;
                youtubedl.RedirectStandardError = false;
                youtubedl.CreateNoWindow = false;
                

            }
            catch (Exception)
            {
                
                WriteLine("You are missing youtube-dl, get it here: https://youtube-dl.org/\n" +
                          "Beaware this program breaks youtube TOS section 9.1 https://www.youtube.com/static?template=terms\n" +
                          "Go get it at your own risk.");
                Debug();
            }

            try
            {
                ffmpeg.WindowStyle = ProcessWindowStyle.Hidden;
                ffmpeg.RedirectStandardOutput = true;
                ffmpeg.RedirectStandardError = true;
                ffmpeg.UseShellExecute = false;
                ffmpeg.CreateNoWindow = true;
                Process.Start(ffmpeg);
                ffmpeg.WindowStyle = ProcessWindowStyle.Normal;
                ffmpeg.RedirectStandardOutput = false;
                ffmpeg.RedirectStandardError = false;
                ffmpeg.CreateNoWindow = false;
            }
            catch (Exception)
            {
                WriteLine("You are missing ffmpeg, get it here: https://ffbinaries.com/downloads");

                Debug();
                Environment.Exit(1);
            }

            try
            {
                ffprobe.WindowStyle = ProcessWindowStyle.Hidden;
                ffprobe.RedirectStandardOutput = true;
                ffprobe.RedirectStandardError = true;
                ffprobe.UseShellExecute = false;
                ffprobe.CreateNoWindow = true;
                Process.Start(ffprobe);
                ffprobe.WindowStyle = ProcessWindowStyle.Normal;
                ffprobe.RedirectStandardOutput = false;
                ffprobe.RedirectStandardError = false;
                ffprobe.CreateNoWindow = false;
            }
            catch (Exception)
            {
                WriteLine("You are missing ffprobe, get it here: https://ffbinaries.com/downloads");

                Debug();
                Environment.Exit(1);
            }
        }

        public void Update()
        {
            Clear();
            WriteLine("Updating please wait...");

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
            WriteLine("link to audio, playlist or 0 to go back");
            Write("#");
            url = ReadLine();
            if (url == "0")
            {
                Clear();
            }
            else
            {
                WriteLine("<Enter> a single audio, \n" +
                          "1 to download full playlist or follow example 1-3,7,9");
                Write("#");
                numb = ReadLine();
                if (numb == "")
                {
                    if (indir == true)
                    {
                        lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" --no-playlist -x --prefer-ffmpeg --ffmpeg-location \"{1}\" --audio-format mp3 \"{2}\"", audiopath, ffmpeg.FileName, url);
                    }
                    else
                    {
                        lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" --no-playlist -x --prefer-ffmpeg --audio-format mp3 \"{1}\"", audiopath, url);
                    }
                }
                else if (numb == "1")
                {
                    if (indir == true)
                    {
                        lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -x --prefer-ffmpeg --ffmpeg-location \"{1}\" --audio-format mp3 \"{2}\"", audiopath, ffmpeg.FileName, url);
                    }
                    else
                    {
                        lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -x --prefer-ffmpeg --audio-format mp3 \"{1}\"", audiopath, url);
                    }
                }
                else
                {
                    if (indir == true)
                    {
                        lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist --playlist-items {1} -x --prefer-ffmpeg --ffmpeg-location \"{2}\" --audio-format mp3 \"{3}\"", audiopath, numb,  ffmpeg.FileName, url);
                    }
                    else
                    {
                        lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist --playlist-items {1} -x --prefer-ffmpeg --audio-format mp3 \"{2}\"", audiopath, numb, url);
                    }
                }
                youtubedl.Arguments = lnk;
                using (var process = Process.Start(youtubedl))
                {
                    process.WaitForExit();
                }
                Write("\a");
            }
        }

        public void Video()
        {
            Clear();
            WriteLine("link to video, playlist or 0 to go back");
            Write("#");
            url = ReadLine();
            if (url == "0")
            {
                Clear();
            }
            else
            {
                WriteLine("<Enter> a single video, \n" +
                          "1 to download full playlist or follow example 1-3,7,9");
                Write("#");
                numb = ReadLine();
                if (numb == "") //no playlist
                {
                    WriteLine("<Enter> for the best quality 1080p + if available, \n" +
                                  "1 for 720p or lower\n" +
                                  "2 to choose yourself");
                    Write("#");
                    qual = ReadLine();
                    if (qual == "1")
                    {
                        if (indir == true)
                        {
                            lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" -f best --no-playlist --ffmpeg-location \"{2}\" --prefer-ffmpeg \"{3}\"", videopath, numb, ffmpeg.FileName, url);
                        }
                        else
                        {
                            lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" -f best --no-playlist --prefer-ffmpeg \"{2}\"", videopath, numb, url);
                        }
                    }
                    else if (qual == "2")
                    {
                        lnk = String.Format("-F --no-playlist {0}", url);
                        youtubedl.Arguments = lnk;
                        using (var process = Process.Start(youtubedl))
                        {
                            process.WaitForExit();
                        }
                        WriteLine("choose video and audio quality by typing numb+numb");
                        Write("#");
                        numb = ReadLine();
                        if (indir == true)
                        {
                            lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" -f \"{1}\" --no-playlist --prefer-ffmpeg --ffmpeg-location \"{2}\" \"{3}\"", videopath, numb, ffmpeg.FileName, url);
                        }
                        else
                        {
                            lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" -f \"{1}\" --no-playlist --prefer-ffmpeg \"{2}\"", videopath, numb, url);
                        }
                    }
                    else
                    {
                        if (indir == true)
                        {
                            lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" -f bestvideo+bestaudio --no-playlist --prefer-ffmpeg --ffmpeg-location \"{1}\" \"{2}\"", videopath, ffmpeg.FileName, url);
                        }
                        else
                        {
                            lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" -f bestvideo+bestaudio --no-playlist --prefer-ffmpeg \"{1}\"", videopath, url);
                        }
                    }
                }
                else
                {
                    WriteLine("<Enter> for the best quality 1080p + if available, \n" +
                              "1 for 720p or lower");
                    Write("#");
                    qual = ReadLine();
                    if (qual == "1")
                    {
                        if (numb == "1")
                        {
                            if (indir == true)
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --ffmpeg-location \"{2}\" --prefer-ffmpeg \"{3}\"", videopath, numb, ffmpeg.FileName, url);
                            }
                            else
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --prefer-ffmpeg \"{2}\"", videopath, numb, url);
                            }
                        }
                        else
                        {
                            if (indir == true)
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --playlist-items {1} --ffmpeg-location \"{2}\" --prefer-ffmpeg \"{3}\"", videopath, numb, ffmpeg.FileName, url);
                            }
                            else
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --playlist-items {1} --prefer-ffmpeg \"{2}\"", videopath, numb, url);
                            }
                        }
                    }
                    else
                    {
                        if (numb == "1")
                        {
                            if (indir == true)
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --ffmpeg-location \"{2}\" --prefer-ffmpeg \"{3}\"", videopath, numb, ffmpeg.FileName, url);
                            }
                            else
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --prefer-ffmpeg \"{2}\"", videopath, numb, url);
                            }
                        }
                        else
                        {
                            if (indir == true)
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --playlist-items {1} --ffmpeg-location \"{2}\" --prefer-ffmpeg \"{3}\"", videopath, numb, ffmpeg.FileName, url);
                            }
                            else
                            {
                                lnk = String.Format("-o \"{0}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --playlist-items {1} --prefer-ffmpeg \"{2}\"", videopath, numb, url);
                            }
                        }
                    }
                }
                youtubedl.Arguments = lnk;
                using (var process = Process.Start(youtubedl))
                {
                    process.WaitForExit();
                }
                Write("\a");
            }
        }

        public void Subtitles()
        {
            Clear();
            WriteLine("link to video with subs or 0 to go back");
            Write("#");
            url = ReadLine();
            if (url == "0")
            {
                Clear();
            }
            else
            {
                WriteLine("<Enter> to download default sub (en), \n" +
                          "1 to choose language");
                Write("#");
                numb = ReadLine();
                if (numb == "")
                {
                    if (indir == true)
                    {
                        lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-format vtt --skip-download --ffmpeg-location \"{1}\" --prefer-ffmpeg \"{2}\"", Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + slash, ffmpeg.FileName, url);
                    }
                    else
                    {
                        lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-format vtt --skip-download --prefer-ffmpeg \"{1}\"", Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + slash, url);
                    }
                }
                else
                {
                    lnk = String.Format("--list-subs --no-playlist {0}", url);
                    youtubedl.Arguments = lnk;
                    using (var process = Process.Start(youtubedl))
                    {
                        process.WaitForExit();
                    }
                    WriteLine("choose sub language");
                    Write("#");
                    numb = ReadLine();
                    if (indir == true)
                    {
                        lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-lang \"{1}\" --sub-format vtt --skip-download --ffmpeg-location \"{2}\" --prefer-ffmpeg \"{3}\"", Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + slash, numb, ffmpeg.FileName, url);
                    }
                    else
                    {
                        lnk = String.Format("-o \"{0}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-lang \"{1}\" --sub-format vtt --skip-download --prefer-ffmpeg \"{2}\"", Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + slash, numb, url);
                    }
                }
                youtubedl.Arguments = lnk;
                using (var process = Process.Start(youtubedl))
                {
                    process.WaitForExit();
                }

                string[] pie = Directory.GetFiles(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "*.vtt");
                string lick = videopath + Path.GetFileNameWithoutExtension(pie[0]) + ".srt";
                lnk = String.Format("-i \"{0}\" \"{1}\"", pie[0], lick);

                ffmpeg.Arguments = lnk;
                using (var process = Process.Start(ffmpeg))
                {
                    process.WaitForExit();
                }

                File.Delete(pie[0]);

                Write("\a");
            }
        }
    }
}
