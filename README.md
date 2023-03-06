{
    "workbench.colorTheme": "Default High Contrast",
    "terminal.integrated.profiles.windows": {
    "Cmder": {
        "path": "${env:windir}\\System32\\cmd.exe",
        "args": ["/k", "E:\\Tools\\cmder\\vendor\\bin\\vscode_init.cmd" ]
    	}
	},
    "terminal.integrated.defaultProfile.windows": "Cmder",
    "[python]": {
        "editor.formatOnType": true
    },
    "terminal.integrated.automationProfile.linux": {},
    "explorer.openEditors.visible": 0,

    "workbench.iconTheme": "vscode-simpler-icons",
    "workbench.sideBar.location": "right",

    "editor.fontFamily": "'Fira Code', 'Microsoft YaHei Mono', Consolas, 'Courier New', monospace",
    // 要啟用連體字型(Fira Code)必須將以下設定打開
    "editor.fontLigatures": true,
    "editor.multiCursorModifier": "ctrlCmd",
    "editor.minimap.enabled": false,
    "editor.minimap.renderCharacters": false,
    "editor.formatOnSave": false,
    "editor.wordWrap": "on",

     "prettier.singleQuote": true,

     "typescript.referencesCodeLens.enabled": false,
     "typescript.updateImportsOnFileMove.enabled": "always",

      "tslint.enable": true,
    "tslint.autoFixOnSave": true,

    "movets.skipWarning": true,
    
    "html.suggest.angular1": false,
    "html.suggest.ionic": false,
    "[html]": {
        "editor.autoIndent": "advanced"
    },

    "csharp.format.enable": false,
    "csharpfixformat.style.enabled": true,
    "csharpfixformat.style.spaces.beforeParenthesis": false,
    "csharpfixformat.style.braces.onSameLine": false,
    "csharpfixformat.style.newline.elseCatch": true,

    "git.autofetch": true,
    "git.enableCommitSigning": false,
    "git.enableSmartCommit": true,
    "git.confirmSync": false,

    "files.associations": {
        "*.csproj": "msbuild"
    },
    "auto-rename-tag.activationOnLanguage": [
        "html",
        "xml",
        "php"
    ],

    "liveServer.settings.donotShowInfoMsg": true,
    "liveServer.settings.donotVerifyTags": true,
    
    "todohighlight.include": [
        "**/*.js",
        "**/*.jsx",
        "**/*.ts",
        "**/*.tsx",
        "**/*.html",
        "**/*.php",
        "**/*.css",
        "**/*.scss",
        "**/*.cs"
    ],

    "docker.languageserver.diagnostics.instructionJSONInSingleQuotes": "warning"
}

