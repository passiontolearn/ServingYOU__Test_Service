@echo off

start cmd /k waitress-serve --port=9999 ServingYOU:api
start http://localhost:9999/songs
