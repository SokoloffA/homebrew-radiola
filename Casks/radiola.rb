cask "radiola" do
  version "5.2.0"
  sha256 "ebe4ee66abdbd73b4208f04399c7bcec552412ab38364fb5daed0744057e35d8"

  url "https://github.com/SokoloffA/radiola/releases/download/v#{version.major_minor}/Radiola-#{version}.dmg"
  # NOTE: When a GitHub release tag is in MAJOR.MINOR.PATCH format, use
  # url "https://github.com/SokoloffA/radiola/releases/download/v#{version}/Radiola-#{version}.dmg"
  # NOTE: When a GitHub release tag is in MAJOR.MINOR format, use
  # url "https://github.com/SokoloffA/radiola/releases/download/v#{version.major_minor}/Radiola-#{version}.dmg"
  name "Radiola"
  desc "Internet radio player for the menu bar"
  homepage "https://github.com/SokoloffA/radiola"

  livecheck do
    url :homepage
    regex(/.*?Radiola[._-]v?(\d+(?:\.\d+)+)\.dmg/i)
    # Use the github_releases strategy to ignore betas with pre-release tags, and match
    # the version in the download url because the release tag can be vMAJOR.MINOR
    # or vMAJOR.MINOR.PATCH but the version is reliably MAJOR.MINOR.PATCH.
    strategy :github_releases do |json, regex|
      json.map do |release|
        next if release["draft"] || release["prerelease"]

        curr_asset = release["assets"]&.find { |asset| asset["browser_download_url"]&.match(regex) }
        next if curr_asset.blank?

        curr_asset["browser_download_url"][regex, 1]
      end
    end
  end

  auto_updates true
  depends_on macos: ">= :big_sur"

  app "Radiola.app"

  uninstall quit: "com.github.SokoloffA.Radiola"

  zap trash: [
    "~/Library/Application Support/com.github.SokoloffA.Radiola",
    "~/Library/Caches/com.github.SokoloffA.Radiola",
    "~/Library/HTTPStorages/com.github.SokoloffA.Radiola",
    "~/Library/Preferences/com.github.SokoloffA.Radiola.plist",
    "~/Library/WebKit/com.github.SokoloffA.Radiola",
  ]
end
