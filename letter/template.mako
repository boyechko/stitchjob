%% -*- mode: latex; -*-
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{parskip}
\usepackage{ragged2e}
\usepackage[hidelinks]{hyperref}
\newcommand\margin{0.75in}
\usepackage[letterpaper,
            bindingoffset=0.2in,
            left=\margin,
            right=\margin,
            top=\margin,
            bottom=\margin,
            footskip=0.25in]{geometry}
\usepackage{graphicx}
\graphicspath{ {./} }

\newcommand{\email}{${letter.contact['email']}}

\begin{document}
\pagenumbering{gobble}

\begin{flushleft}
${letter.contact['name']}\\\
${letter.contact['location']}\\\
${letter.contact['phone']}\\\
\href{mailto:${letter.contact['email']}}{${letter.contact['email']}}\\\
% if 'date' in letter.metadata:
  ${letter.metadata['date']}
% else:
  \today
% endif
\end{flushleft}

\vspace{0.5cm}

\begin{flushleft}
% if 'recipient' in letter.metadata:
  ${letter.metadata['recipient']}\\\
% endif
% if 'company' in letter.metadata:
  ${letter.metadata['company']}\\\
% endif
% if 'address' in letter.metadata:
  ${letter.metadata['address']}\\\
% endif
% if 'location' in letter.metadata:
  ${letter.metadata['location']}\\\
% endif
\end{flushleft}
\vspace{1cm}

\raggedright
% if 'salutation' in letter.metadata:
  ${letter.metadata['salutation']}%
% elif 'recipient' in letter.metadata:
  Dear ${letter.metadata['recipient']},%
% else:
  Dear Hiring Manager,%
% endif

${letter.content}

\begin{flushleft}
% if 'closing' in letter.metadata:
  ${letter.metadata['closing']}\\\
% else:
  Sincerely,\\\
% endif
% if letter.signature_image:
  \vspace{1ex}
  \includegraphics[height=2em]{${letter.signature_image}}\\\
  \vspace{1ex}
% else:
  \vspace{1em}
% endif
% if 'signature' in letter.metadata:
  ${letter.metadata['signature']}
% else:
  ${letter.contact['name']}
% endif
\end{flushleft}

\end{document}
