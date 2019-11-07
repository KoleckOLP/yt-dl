#/bin/bash

cd ..
dotnet publish --runtime osx-x64
cd bin/Debug/netcoreapp2.2/osx-x64/publish
chmod 777 yt-dl

