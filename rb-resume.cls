\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rb-resume}[2025/06/29 RB's Custom Resume Class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[12pt]{article}

\RequirePackage[utf8]{inputenc}
\RequirePackage{ifthen}
\RequirePackage[hidelinks]{hyperref} % Hide link borders
\RequirePackage{graphicx}

\RequirePackage{geometry}
\newcommand\margin{0.5in}
\geometry{letterpaper,
          bindingoffset=0.2in,
          left=\margin,
          right=\margin,
          top=\margin,
          bottom=\margin,
          footskip=0.25in}

\RequirePackage{parskip}

\setlength{\smallskipamount}{8pt plus 3pt minus 3pt}
\setlength{\medskipamount}{12pt plus 2pt minus 2pt}
\setlength{\bigskipamount}{24pt plus 8pt minus 8pt}

\RequirePackage{enumitem}
\setlist[itemize]{noitemsep,leftmargin=5mm}

\RequirePackage{xcolor}
\definecolor{customblue}{HTML}{3E64FF}
\definecolor{lightgray}{gray}{0.01}

%\usepackage[sfdefault,light,medium]{josefin}
\usepackage{tgheros}
\usepackage[T1]{fontenc}
\renewcommand\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif

\RequirePackage{titlesec}
%\titleformat{\section}{\large\color{customblue}\bfseries}{}{0em}{}
\titleformat*{\section}{\large\bfseries\color{customblue}\scshape}
\titlespacing{\section}{0pt}{\smallskipamount}{\smallskipamount}

\titleformat*{\subsection}{\normalsize\bfseries}
\titleformat*{\subsubsection}{\normalize\scshape}
\titleformat*{\paragraph}{\normalsize}
\titleformat*{\subparagraph}{\normalsize}

\newcommand{\heading}[1]{{\Huge\color{black}\textbf{#1}}}
\newcommand{\datedsubsection}[2]{\subsection*{#1 \hfill \textmd{\textcolor{customblue}{#2}}}}
\newcommand{\degree}[5]{\subsection*{#1 \textmd{(#2), #3, #4 \hfill \textcolor{customblue}{#5}}}}

\RequirePackage{xparse}
\RequirePackage{etoolbox}
\NewDocumentCommand{\organization}{ m o o }{%
   \textsl{#1%
     \IfValueT{#2}{\IfBlankTF{#2}{}{ (#2)}}%
     \IfValueT{#3}{\IfBlankTF{#3}{}{\\#3}}%
   }%
}

\RequirePackage{multicol}
\newenvironment{skills}[1]{%
  \begin{multicols}{2}[\section*{#1}]%
    \begin{itemize}%
}{%
    \end{itemize}%
  \end{multicols}%
}

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

\AtBeginDocument{
  \begin{center}
    \heading{\name}\\
    \smallskip
    {\href{mailto:\email}{\email}}\enspace$\mid$\enspace\phone\enspace$\mid$\enspace\location \\
    \ifdef{\linkedin}{\href{https://\linkedin}{\linkedin}}{}
    \ifdef{\github}{\enspace$\mid$\enspace\href{https://\github}{\github}}{}
  \end{center}

  \raggedright
}

\endinput
