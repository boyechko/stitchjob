\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rb-resume}[2025/06/29 RB's Custom Resume Class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[12pt]{article}

\RequirePackage[utf8]{inputenc}
\RequirePackage{fontspec}
\RequirePackage{lmodern}
\RequirePackage{parskip}
\RequirePackage{paracol}
\RequirePackage{ragged2e}
\RequirePackage{xcolor}
\RequirePackage[hidelinks]{hyperref} % Hide link borders
\RequirePackage{graphicx}
\RequirePackage{ifthen}

% Geometry
\newcommand\margin{0.5in}
\RequirePackage{geometry}
\geometry{letterpaper,
    bindingoffset=0.2in,
    left=\margin,
    right=\margin,
    top=\margin,
    bottom=\margin,
    footskip=0.25in}
\columnratio{0.65, 0.35}
\setlength\columnsep{0.05\textwidth}
\setlength\parindent{0pt}
\setlength{\smallskipamount}{8pt plus 3pt minus 3pt}
\setlength{\medskipamount}{12pt plus 2pt minus 2pt}
\setlength{\bigskipamount}{24pt plus 8pt minus 8pt}

\RequirePackage{enumitem}
\setlist[itemize]{noitemsep,leftmargin=5mm}

%===============================================================================
% Style
%===============================================================================

% No page numbers
\pagestyle{empty}

% Colors

\definecolor{customblue}{HTML}{3E64FF}
\definecolor{lightgray}{gray}{0.01}

% Sections

\RequirePackage{titlesec}
%\titleformat{\section}{\large\color{customblue}\bfseries}{}{0em}{}
\titleformat*{\section}{\large\sffamily\scshape}
\titlespacing{\section}{0pt}{\smallskipamount}{\smallskipamount}
\titleformat*{\subsection}{\large\sffamily}
\titleformat*{\subsubsection}{\large\bfseries\sffamily}
\titleformat*{\paragraph}{\large\bfseries\sffamily}
\titleformat*{\subparagraph}{\large\bfseries\sffamily}

\newcommand{\heading}[1]{{\Huge\color{black}\textbf{#1}}}
\newcommand{\experience}[2]{\subsection*{#1 \hfill \textcolor{customblue}{#2}}}
%\newcommand{\consulting}[1]{\ifdef{\consultingFlag}{#1}{}}
%\newcommand{\tech}[1]{\ifdef{\techFlag}{#1}{}}
%\newcommand{\gpa}[1]{\ifdef{\gpaFlag}{#1}{}}

%\RequirePackage{pifont}
%\newenvironment{bullets}{\begin{dinglist}}{\end{dinglist}}

% Define variables
\newcommand{\name}{}
\newcommand{\email}{}
\newcommand{\phone}{}
\newcommand{\location}{}
%\newcommand{\linkedin}{}
%\newcommand{\github}{}

% Setters
\newcommand{\setname}[1]{\renewcommand{\name}{#1}}
\newcommand{\setemail}[1]{\renewcommand{\email}{#1}}
\newcommand{\setphone}[1]{\renewcommand{\phone}{#1}}
\newcommand{\setlocation}[1]{\renewcommand{\location}{#1}}
\newcommand{\setlinkedin}[1]{\renewcommand{\linkedin}{#1}}
\newcommand{\setgithub}[1]{\renewcommand{\github}{#1}}

% Default header
\AtBeginDocument{
  \begin{center}
    \heading{\name}\\
    \smallskip
    {\href{mailto:\email}{\email}}\enspace$\mid$\enspace\phone\enspace$\mid$\enspace\location \\
    \ifdef{\linkedin}{\href{https://\linkedin}{\linkedin}}{}
    \ifdef{\github}{\enspace$\mid$\enspace\href{https://\github}{\github}}{}
  \end{center}

  \raggedright
  % For some raggedness, but still hyphenated sometimes:
  %\RaggedRight
}

\endinput

