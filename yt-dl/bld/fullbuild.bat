@echo on

cd ..

dotnet publish -r win-x64 -c Release

dotnet publish -r osx-x64 -c Release

dotnet publish -r linux-x64 -c Release