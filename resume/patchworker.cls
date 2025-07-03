\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{patchworker}[2025/06/29 Patchworker Resume Class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[12pt]{article}

\RequirePackage[utf8]{inputenc}
\RequirePackage{ifthen}
\RequirePackage[hidelinks]{hyperref} % Hide link borders
\RequirePackage{graphicx}

\pagestyle{empty}

\RequirePackage{geometry}
\newcommand\margin{0.75in}
\geometry{letterpaper,
          bindingoffset=0pt,
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

\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
%\RequirePackage{tgheros}
%\RequirePackage[sfdefault,light,medium]{josefin}
%\renewcommand\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
\RequirePackage{fontawesome}

\RequirePackage{titlesec}
%\titleformat{\section}{\large\color{customblue}\bfseries}{}{0em}{}
\titleformat*{\section}{\large\bfseries\color{customblue}\scshape}
\titlespacing{\section}{0pt}{\smallskipamount}{\smallskipamount}

\titleformat*{\subsection}{\normalsize\bfseries}
\titleformat*{\subsubsection}{\normalsize\itshape}
\titleformat*{\paragraph}{\normalsize}
\titleformat*{\subparagraph}{\normalsize}

\newcommand{\heading}[1]{{\Huge\color{black}\textbf{#1}}}
\newcommand{\datedsubsection}[2]{\subsection*{#1 \hfill \textmd{\textcolor{customblue}{#2}}}}
\newcommand{\degree}[5]{\textbf{#1} \textmd{(#2), #3, #4 \hfill \textcolor{customblue}{#5}}\\}

\RequirePackage{xparse}
\RequirePackage{etoolbox}
\NewDocumentCommand{\organization}{ m o o }{%
   \textsl{#1%
     \IfValueT{#2}{\IfBlankTF{#2}{}{ (#2)}}%
     \IfValueT{#3}{\IfBlankTF{#3}{}{\\#3}}%
   }%
}

\RequirePackage{multicol}
\newenvironment{skills}{%
  \begin{multicols}{2}%
    \begin{itemize}%
}{%
    \end{itemize}%
  \end{multicols}%
}

\RequirePackage{keyval}
\RequirePackage{etoolbox}       % for \ifstrempty

% Declare keys and associated macros
\define@key{profile}{name}{\def\profile@name{#1}}
\define@key{profile}{email}{\def\profile@email{#1}}
\define@key{profile}{phone}{\def\profile@phone{#1}}
\define@key{profile}{location}{\def\profile@location{#1}}
\define@key{profile}{linkedin}{\def\profile@linkedin{#1}}
\define@key{profile}{github}{\def\profile@github{#1}}

% Provide default (empty) values
\def\profile@name{}
\def\profile@email{}
\def\profile@phone{}
\def\profile@location{}
\def\profile@linkedin{}
\def\profile@github{}

% Setter command
\newcommand{\setprofile}[1]{\setkeys{profile}{#1}}
\newcommand{\iconify}[2]{\enspace\mbox{#1\enspace#2}}
\newcommand{\linkedin}[1]{\href{https://www.linkedin.com/in/#1}{#1}}
\newcommand{\github}[1]{\href{https://www.github.common/#1}{#1}}

\newcommand{\printprofile}{%
  \begin{center}
    \heading{\profile@name}\\
    \smallskip
    \iconify{\faEnvelope}{\href{mailto:\profile@email}{\profile@email}}%
    \iconify{\faPhone}{\profile@phone}%
    \iconify{\faLocationArrow}{\profile@location}%
    \linebreak[0]%
    \ifstrempty{\profile@linkedin}{}{%
      \iconify{\faLinkedinSquare}{\linkedin{\profile@linkedin}}%
    }%
    \ifstrempty{\profile@github}{}{%
      \iconify{\faGithub}{\github{\profile@github}}%
    }%
  \end{center}
  \raggedright
}

\AtBeginDocument{%
  \printprofile
  \raggedright
}

\endinput
