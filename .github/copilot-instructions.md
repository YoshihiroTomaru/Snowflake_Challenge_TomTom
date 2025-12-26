# AI Assistant Instructions

このファイルには、AI アシスタント（GitHub Copilot等）がこのプロジェクトで作業する際に従うべきルールとガイドラインを記載しています。

## Git Workflow Rules

### ブランチ戦略

- **mainブランチへの直接コミットは禁止**
- 必ず feature ブランチを作成してから作業を開始する
- Pull Request を通じてのみ main ブランチにマージする

### 作業フロー

1. 新しい機能や修正を開始する際：
   ```bash
   git checkout -b feature/<feature-name>
   ```

2. 変更をコミット：
   ```bash
   git add <files>
   git commit -m "descriptive message"
   ```

3. feature ブランチをリモートにプッシュ：
   ```bash
   git push -u origin feature/<feature-name>
   ```

4. GitHub で Pull Request を作成

5. レビュー後、PR を通じて main にマージ

### ブランチ命名規則

- 新機能: `feature/<description>`
- バグ修正: `fix/<description>`
- ドキュメント: `docs/<description>`
- リファクタリング: `refactor/<description>`

### コミットメッセージ

- 英語で記述
- 簡潔で明確な説明
- 複数の変更がある場合は箇条書きで詳細を追加

例：
```
Add OAuth browser authentication support with PKCE

- Implemented browser-based OAuth authentication flow
- Added oauth.py module for token management
- Updated documentation with setup instructions
```

## プロジェクト構成

このリポジトリには3つの主要コンポーネントがあります：

1. **python_client/**: キーペア認証とOAuth認証をサポートするPythonクライアント
2. **cortex_agent_call/**: PAT認証専用のシンプルなCortex Agent APIクライアント
3. **mcp_server_setup/**: VS Code用のMCP Server連携設定

### 新しいフォルダ/コンポーネントを追加する際のルール

1. **仮想環境の配置**
   - 新しいフォルダを作成する際は、そのフォルダ内に仮想環境を作成する
   - プロジェクト直下に `.venv` を作らない
   - 例: `new_component/.venv`

2. **ドキュメントの作成**
   - 新しいフォルダには必ず `README.md` を作成する
   - セットアップ手順、使い方、ファイル構成を記載する

3. **ルートREADME.mdの更新**
   - 新しいコンポーネントを追加したら、プロジェクト直下の `README.md` を更新する
   - コンポーネントのリストに新しい項目を追加する
   - 簡潔な説明とリンクを含める

例：
```bash
# 新しいコンポーネントの作成
mkdir new_component
cd new_component
python -m venv .venv
.venv\Scripts\activate
# README.mdを作成
# ルートのREADME.mdも更新
```

## コーディング規約

- Python: PEP 8 に従う
- 日本語のコメントとドキュメントを使用（ユーザーが日本語話者のため）
- `.env` ファイルは Git にコミットしない
- 秘密情報（トークン、パスワード）はコードに埋め込まない

## 環境固有の注意事項

- OS: Windows
- シェル: PowerShell
- エディタ: VS Code
- Python仮想環境: `.venv`
