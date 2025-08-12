\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{stitched}[2025/06/29 Stitchjob Resume Class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[12pt]{article}

\RequirePackage[utf8]{inputenc}
\RequirePackage{ifthen}
\RequirePackage[hidelinks]{hyperref} % Hide link borders
\RequirePackage{graphicx}

%
% Page Layout
%

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

%
% Vertical Spacing
%

\RequirePackage{parskip}

\setlength{\smallskipamount}{8pt plus 3pt minus 3pt}
\setlength{\medskipamount}{12pt plus 2pt minus 2pt}
\setlength{\bigskipamount}{24pt plus 8pt minus 8pt}

% Lists

\RequirePackage{enumitem}
\setlist[itemize]{noitemsep,leftmargin=5mm}

% Colors

\RequirePackage{xcolor}
\definecolor{customblue}{HTML}{3869FF}
\definecolor{lightgray}{gray}{0.01}

% Fonts

\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
%\RequirePackage{tgheros}
%\RequirePackage[sfdefault,light,medium]{josefin}
%\renewcommand\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
\RequirePackage{fontawesome}

% Section Styling

\RequirePackage{titlesec}
\titleformat*{\section}{\large\color{customblue}\scshape}
\titlespacing{\section}{0pt}{\smallskipamount}{\smallskipamount}

\titleformat*{\subsection}{\normalsize\bfseries}
\titleformat*{\subsubsection}{\normalsize\itshape}

%
% New Commands
%

\RequirePackage{xparse}
\RequirePackage{etoolbox}

\newcommand{\heading}[1]{{\Huge\color{black}\textbf{#1}}}

% Education

\newenvironment{education}{%
  \begin{enumerate}[label={},left=0pt .. 0pt,itemindent=0pt,nosep]%
}{%
  \end{enumerate}
}

% \degree{degree}{major}{institution}{location}
\newcommand{\degree}[5]{%
  \item {\textbf{#1} \textmd{(#2), #3, #4 \hfill \textcolor{customblue}{#5}}\\}%
}

% Syntax: \experience{dates}{role}{organization}[location]
\NewDocumentCommand{\experience}{ m m m o }{%
  \subsection*{#2 \hfill \textmd{\textcolor{customblue}{#1}}%
    \\%
    \textmd{\textsl{#3\IfValueT{#4}{\IfBlankTF{#4}{}{ (#4)}}}}%
  }
}

\newcommand{\blurb}[1]{\textit{#1}}

\RequirePackage{multicol}
\newenvironment{skills}{%
  \begin{multicols}{2}%
    \begin{itemize}%
}{%
    \end{itemize}%
  \end{multicols}%
}

%
% Candidate Profile
%

\RequirePackage{keyval}
\RequirePackage{etoolbox}       % for \ifstrempty

% Declare keys and associated macros
\define@key{profile}{name}{\def\profile@name{#1}}
\define@key{profile}{email}{\def\profile@email{#1}}
\define@key{profile}{phone}{\def\profile@phone{#1}}
\define@key{profile}{location}{\def\profile@location{#1}}
\define@key{profile}{linkedin}{\def\profile@linkedin{#1}}
\define@key{profile}{github}{\def\profile@github{#1}}
\define@key{profile}{website}{\def\profile@website{#1}}

% Provide default (empty) values
\def\profile@name{}
\def\profile@email{}
\def\profile@phone{}
\def\profile@location{}
\def\profile@linkedin{}
\def\profile@github{}
\def\profile@website{}

% Setter command
\newcommand{\setprofile}[1]{%
  \setkeys{profile}{#1}%
  \hypersetup{%
    pdfauthor=\profile@name,%
    pdftitle={Resume - \profile@name},%
    pdfdisplaydoctitle=true,%
    pdfcreator=Stitchjob%
  }
}

% Commands for typesetting the profile
\newcommand{\bluehref}[2]{\href{#1}{\textcolor{blue}{\underline{\smash{#2}}}}}
\newcommand{\iconify}[2]{\enspace\mbox{#1\enspace#2}}

\newcommand{\emaillink}[1]{\bluehref{mailto:#1}{#1}}
\newcommand{\linkedinlink}[1]{\bluehref{https://www.linkedin.com/in/#1}{#1}}
\newcommand{\githublink}[1]{\bluehref{https://www.github.com/#1}{#1}}
\newcommand{\websitelink}[1]{\bluehref{https://#1}{#1}}

\newcommand{\printprofile}{%
  \begin{center}
    \heading{\profile@name}\\
    \smallskip
    \iconify{\faEnvelope}{\emaillink{\profile@email}}%
    \iconify{\faPhone}{\profile@phone}%
    % alternative icons: \faHome, \faMap, \faMapO, \faMapPin, \faMapPin
    \iconify{\faLocationArrow}{\profile@location}%
    \linebreak[0]%
    \ifdefempty{\profile@linkedin}{}{%
      \iconify{\faLinkedinSquare}{\linkedinlink{\profile@linkedin}}%
    }%
    \ifdefempty{\profile@github}{}{%
      \iconify{\faGithub}{\githublink{\profile@github}}%
    }%
    % alternative icons: \faMousePointer, \faBookmarkO
    \ifdefempty{\profile@website}{}{%
      \iconify{\faBookmark}{\websitelink{\profile@website}}%
    }%
  \end{center}
}

\AtBeginDocument{%
  \pdfinterwordspaceon
  \printprofile
  \raggedright
}

\endinput
